#!/bin/bash
# Autonomous Campus Rover - Dependency Installation Script

echo "Updating APT packages..."
sudo apt-update && sudo apt upgrade -y

echo "Installing system dependencies for OpenCV and audio..."
sudo apt install -y build-essential cmake pkg-config \
    libjpeg-dev libtiff5-dev libjasper-dev libpng-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev \
    libfontconfig1-dev libcairo2-dev \
    libgdk-pixbuf2.0-dev libpango1.0-dev \
    libgtk2.0-dev libgtk-3-dev \
    libatlas-base-dev gfortran \
    python3-dev python3-pip python3-venv \
    portaudio19-dev

echo "Setting up Python virtual environment..."
cd ../pi_core
python3 -m venv venv
source venv/bin/activate

echo "Installing Python pip dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! To start the rover, run:"
echo "cd ../pi_core && source venv/bin/activate && python main.py"
