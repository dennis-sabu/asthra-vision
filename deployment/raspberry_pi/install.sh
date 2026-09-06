#!/bin/bash

# ASTHRA Vision - Raspberry Pi 4 Production Installation Script
# This script prepares the system for running the production vision system.

set -e # Exit on error

echo "--------------------------------------------------"
echo "ASTHRA Vision: Raspberry Pi 4 Production Setup"
echo "--------------------------------------------------"

# 1. Update system packages
echo "[1/7] Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install production system dependencies
echo "[2/7] Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libatlas-base-dev \
    git \
    wget \
    cmake \
    build-essential

# 3. Create Python virtual environment
echo "[3/7] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists. Skipping."
fi

# 4. Install Python dependencies
echo "[4/7] Installing production Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Prepare for NCNN inference
echo "[5/7] Preparing for NCNN inference..."
# Ensure the ultralytics package is fully installed for exporting/loading
pip install ultralytics

# 6. Prepare directory structure
echo "[6/7] Creating models directory structure..."
mkdir -p models/development
mkdir -p models/production

# 7. Final check
echo "[7/7] Verifying installation..."
if [ -f "venv/bin/python" ]; then
    echo "--------------------------------------------------"
    echo "SUCCESS: ASTHRA Vision production environment installed!"
    echo "Next steps:"
    echo "1. Setup the production model: ./deployment/raspberry_pi/setup_model.sh"
    echo "2. Configure environment: cp deployment/raspberry_pi/.env.example .env"
    echo "3. Run the system: ./deployment/raspberry_pi/run.sh"
    echo "--------------------------------------------------"
else
    echo "ERROR: Installation failed. Virtual environment not found."
    exit 1
fi
