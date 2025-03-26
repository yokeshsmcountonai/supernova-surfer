# Use a Debian-based ARM64 image
FROM --platform=linux/arm64 debian:bullseye-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    unzip \
    libpq-dev \
    libgl1 \
    libxkbcommon-x11-0 \
    qt5-qmake \
    qtbase5-dev \
    libqt5webengine5 \
    libqt5webenginewidgets5 \
    libqt5webchannel5 \
    libqt5positioning5 \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY ./main.zip /app
COPY ./requirements.txt /app

# Unzip the main source code
RUN unzip main.zip && rm main.zip

# Install dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt


CMD ["python3", "main.py"]