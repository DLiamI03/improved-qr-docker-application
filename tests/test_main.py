"""Tests for the QR code generator main module."""
import argparse
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from main import (
    create_directory,
    generate_qr_code,
    is_valid_url,
    main,
    setup_logging,
)


class TestSetupLogging:
    """Test logging setup functionality."""

    @patch("main.logging.basicConfig")
    def test_setup_logging_called_correctly(self, mock_basic_config):
        """Test that logging is configured correctly."""
        setup_logging()
        mock_basic_config.assert_called_once()


class TestCreateDirectory:
    """Test directory creation functionality."""

    def test_create_directory_success(self, tmp_path):
        """Test successful directory creation."""
        new_dir = tmp_path / "test_dir"
        create_directory(new_dir)
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_create_directory_already_exists(self, tmp_path):
        """Test directory creation when directory already exists."""
        existing_dir = tmp_path / "existing_dir"
        existing_dir.mkdir()
        create_directory(existing_dir)  # Should not raise an exception
        assert existing_dir.exists()

    @patch("main.logging.error")
    @patch("main.sys.exit")
    def test_create_directory_failure(self, mock_exit, mock_log_error):
        """Test directory creation failure."""
        # Try to create a directory in a path that will fail
        invalid_path = Path("/invalid/path/that/cannot/be/created")

        with patch(
            "pathlib.Path.mkdir", side_effect=OSError("Permission denied")
        ):
            create_directory(invalid_path)

        mock_log_error.assert_called_once()
        mock_exit.assert_called_once_with(1)


class TestIsValidUrl:
    """Test URL validation functionality."""

    def test_valid_url_http(self):
        """Test validation of valid HTTP URL."""
        assert is_valid_url("http://example.com") is True

    def test_valid_url_https(self):
        """Test validation of valid HTTPS URL."""
        assert is_valid_url("https://github.com/username") is True

    @patch("main.logging.error")
    def test_invalid_url(self, mock_log_error):
        """Test validation of invalid URL."""
        invalid_url = "not_a_valid_url"
        result = is_valid_url(invalid_url)

        assert result is False
        mock_log_error.assert_called_once_with(
            f"Invalid URL provided: {invalid_url}"
        )

    @patch("main.logging.error")
    def test_empty_url(self, mock_log_error):
        """Test validation of empty URL."""
        empty_url = ""
        result = is_valid_url(empty_url)

        assert result is False
        mock_log_error.assert_called_once_with(
            f"Invalid URL provided: {empty_url}"
        )


class TestGenerateQrCode:
    """Test QR code generation functionality."""

    @patch("main.is_valid_url")
    @patch("main.qrcode.QRCode")
    @patch("main.logging.info")
    def test_generate_qr_code_success(
        self, mock_log_info, mock_qr_class, mock_is_valid_url, tmp_path
    ):
        """Test successful QR code generation."""
        mock_is_valid_url.return_value = True
        mock_qr = MagicMock()
        mock_qr_class.return_value = mock_qr
        mock_img = MagicMock()
        mock_qr.make_image.return_value = mock_img

        test_file = tmp_path / "test_qr.png"
        url = "https://github.com/username"

        with patch("builtins.open", create=True) as mock_open:
            generate_qr_code(url, test_file)

        mock_is_valid_url.assert_called_once_with(url)
        mock_qr.add_data.assert_called_once_with(url)
        mock_qr.make.assert_called_once_with(fit=True)
        mock_img.save.assert_called_once()
        mock_log_info.assert_called_once()

    @patch("main.is_valid_url")
    def test_generate_qr_code_invalid_url(self, mock_is_valid_url, tmp_path):
        """Test QR code generation with invalid URL."""
        mock_is_valid_url.return_value = False

        test_file = tmp_path / "test_qr.png"
        url = "invalid_url"

        generate_qr_code(url, test_file)

        # Should return early without creating file
        assert not test_file.exists()

    @patch("main.is_valid_url")
    @patch("main.qrcode.QRCode")
    @patch("main.logging.error")
    def test_generate_qr_code_exception(
        self, mock_log_error, mock_qr_class, mock_is_valid_url, tmp_path
    ):
        """Test QR code generation with exception."""
        mock_is_valid_url.return_value = True
        mock_qr_class.side_effect = Exception("Test exception")

        test_file = tmp_path / "test_qr.png"
        url = "https://github.com/username"

        generate_qr_code(url, test_file)

        mock_log_error.assert_called_once()


class TestMain:
    """Test main function functionality."""

    @patch("main.setup_logging")
    @patch("main.create_directory")
    @patch("main.generate_qr_code")
    @patch("main.Path.cwd")
    def test_main_default_url(
        self,
        mock_cwd,
        mock_generate_qr,
        mock_create_dir,
        mock_setup_logging,
        tmp_path,
    ):
        """Test main function with default URL."""
        mock_cwd.return_value = tmp_path

        with patch("sys.argv", ["main.py"]):
            main()

        mock_setup_logging.assert_called_once()
        mock_create_dir.assert_called_once()
        mock_generate_qr.assert_called_once()

    @patch("main.setup_logging")
    @patch("main.create_directory")
    @patch("main.generate_qr_code")
    @patch("main.Path.cwd")
    def test_main_custom_url(
        self,
        mock_cwd,
        mock_generate_qr,
        mock_create_dir,
        mock_setup_logging,
        tmp_path,
    ):
        """Test main function with custom URL."""
        mock_cwd.return_value = tmp_path
        custom_url = "https://github.com/custom"

        with patch("sys.argv", ["main.py", "--url", custom_url]):
            main()

        mock_setup_logging.assert_called_once()
        mock_create_dir.assert_called_once()
        mock_generate_qr.assert_called_once()

        # Check if the custom URL was passed to generate_qr_code
        args, kwargs = mock_generate_qr.call_args
        assert custom_url in args


class TestEnvironmentVariables:
    """Test environment variable handling."""

    def test_default_values(self):
        """Test default values when environment variables are not set."""
        # Import after clearing environment variables
        with patch.dict(os.environ, {}, clear=True):
            import importlib
            import main

            importlib.reload(main)

            assert main.QR_DIRECTORY == "qr_codes"
            assert main.FILL_COLOR == "red"
            assert main.BACK_COLOR == "white"

    def test_custom_environment_variables(self):
        """Test custom environment variable values."""
        env_vars = {
            "QR_CODE_DIR": "custom_qr",
            "FILL_COLOR": "blue",
            "BACK_COLOR": "yellow",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            import importlib
            import main

            importlib.reload(main)

            assert main.QR_DIRECTORY == "custom_qr"
            assert main.FILL_COLOR == "blue"
            assert main.BACK_COLOR == "yellow"


if __name__ == "__main__":
    pytest.main([__file__])
