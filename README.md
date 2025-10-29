# Docker and Python QR Code Generator

🔗 **Repository**: https://github.com/DLiamI03/improved-qr-docker-application

For this assignment you will be combining Docker with Python to create a program that generates a QR code PNG file that contains a URL. The QR code can be viewed with the camera on your phone to allow a user to click on it and send them to the target website. You must make your program generate a QR code that takes someone to your GitHub homepage i.e. https://github.com/DLiamI03

This project includes professional development practices including:

• Code formatting with Black
• Linting with Flake8
• Type checking with MyPy
• Testing with Pytest (98% coverage)
• Proper project configuration with pyproject.toml

## Setup

1. Goto Docker.com and Install docker - https://www.docker.com/get-started/
2. Signup for your own Docker account
3. Install Python dependencies: `pip install -r requirements.txt`

## Local Development

### Running the QR Code Generator

```bash
# Generate QR code with default URL
python main.py

# Generate QR code with custom URL
python main.py --url https://github.com/yourusername
```

### Development Tools

```bash
# Format code
python -m black .

# Check code style
python -m flake8 main.py tests/

# Type checking
python -m mypy main.py

# Run tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=main --cov-report=term-missing
```

## Docker Usage

### Building the Image

```bash
docker build -t my-qr-app .
```

This command builds a Docker image named `my-qr-app` from the Dockerfile in the current directory (`.`).

### Running the Container with Default Settings

```bash
docker run -d --name qr-generator my-qr-app
```

Runs your QR code generator application in detached mode (`-d`) with a container named `qr-generator`.

### Setting Environment Variables for QR Code Customization

```bash
docker run -d --name qr-generator \
  -e QR_DATA_URL='https://example.com' \
  -e QR_CODE_DIR='qr_codes' \
  -e QR_CODE_FILENAME='exampleQR.png' \
  -e FILL_COLOR='blue' \
  -e BACK_COLOR='yellow' \
  my-qr-app
```

Customizes the QR code generation settings through environment variables.

### Sharing a Volume for QR Code Output

```bash
docker run -d --name qr-generator \
  -v /host/path/for/qr_codes:/app/qr_codes \
  my-qr-app
```

Mounts a host directory to the container for storing QR codes.

### Combining Volume Sharing and Environment Variables

```bash
docker run -d --name qr-generator \
  -e QR_CODE_DIR='qr_codes' \
  -e FILL_COLOR='blue' \
  -e BACK_COLOR='yellow' \
  -v /host/path/for/qr_codes:/app/qr_codes \
  my-qr-app
```

A comprehensive command that configures the QR code settings and mounts volumes for QR codes.

## Setting the arg for the url from the terminal

```bash
docker run -v .:/app my-qr-app --url https://github.com/yourusername
```

This is how you would set the url for the qr code

### Basic Docker Commands Explained

**Building an Image**

```bash
docker build -t image_name .
```

Builds a Docker image with the tag `image_name` from the Dockerfile in the current directory.

**Running a Container**

```bash
docker run --name container_name image_name
```

Runs a container named `container_name` from `image_name` in the foreground / attached mode

```bash
docker run -d --name container_name image_name
```

Runs a container named `container_name` from `image_name` in detached mode

**Listing Running Containers**

```bash
docker ps
```

Shows a list of all running containers.

**Stopping a Container**

```bash
docker stop container_name
```

**Removing a Container**

```bash
docker rm container_name
```

**Listing Docker Images**

```bash
docker images
```

Lists all Docker images available on your machine.

**Removing a Docker Image**

```bash
docker rmi image_name
```

Removes a Docker image.

**Viewing Logs of a Container**

```bash
docker logs container_name
```

Displays the logs from a running or stopped container.

These commands cover the essentials of building, running, and managing Docker containers and images, along with specific examples for your QR code generation application.

## Docker Compose Usage

You can also use Docker Compose for easier container management:

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop and remove containers
docker-compose down
```

## Environment Variables

The application supports the following environment variables:

- `QR_CODE_DIR`: Directory to save QR codes (default: "qr_codes")
- `FILL_COLOR`: Fill color for QR code (default: "red")
- `BACK_COLOR`: Background color for QR code (default: "white")

## Submission Requirements:

1. ✅ **QR Code Generated**: Successfully creates QR codes linking to GitHub profiles
2. ✅ **Repository Created**: Live at https://github.com/DLiamI03/improved-qr-docker-application
3. ✅ **Docker Implementation**: Complete Docker setup with Dockerfile and docker-compose.yml
4. ✅ **Professional Development**: Black formatting, Flake8 linting, MyPy type checking, Pytest testing

### Generated QR Codes:
The application successfully generates QR codes. Example usage:
```bash
python main.py --url https://github.com/DLiamI03
```

### Sample Log Output:
```
2025-10-28 21:17:33,323 - INFO - QR code successfully saved to /Users/liam/improved-qr-docker-2024/qr_codes/QRCode_20251028211733.png
```

## Lesson Video

1. [Scaling and Backend Software Engineering](https://youtu.be/v3LxCmYQVS4)
2. [Docker and Cloud Computing Intro](https://youtu.be/FpeGzRkBycw)

## Readings / Tutorials - No, really you should read these

• [Containerization vs. Virtualization](https://www.liquidweb.com/kb/virtualization-vs-containerization/)
• [Official docker Getting Started - Go over all the sections](https://docs.docker.com/guides/get-started/)
• [Entrypoint vs. CMD vs. RUN](https://codewithyury.com/docker-run-vs-cmd-vs-entrypoint/)
• [Make QR with Python](https://towardsdatascience.com/generate-qrcode-with-python-in-5-lines-42eda283f325)
• [Make Dockerfile](https://thenewstack.io/docker-basics-how-to-use-dockerfiles/)
• [Args and Environment Variables in Docker](https://vsupalov.com/docker-arg-env-variable-guide/)

## Project Structure

```
improved-qr-docker-application/
├── tests/
│   ├── __init__.py
│   └── test_main.py            # Unit tests (15 tests, 100% passing)
├── qr_codes/                   # Generated QR code output directory
├── .dockerignore               # Docker ignore file
├── .env.example               # Environment variables template
├── .gitignore                  # Git ignore file
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml         # Docker Compose configuration
├── main.py                     # Main application code
├── pyproject.toml             # Project configuration
├── pytest.ini                # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).