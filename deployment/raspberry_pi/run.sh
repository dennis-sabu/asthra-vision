#!/bin/bash

# ASTHRA Vision - Raspberry Pi 4 Production Run Script

# 1. Locate project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "Starting ASTHRA Vision Production System..."

# 2. Load Environment Configuration
if [ -f ".env" ]; then
    echo "Loading configuration from .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "No .env file found. Using default configuration from config.py."
fi

# 3. Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Please run ./deployment/raspberry_pi/install.sh first."
    exit 1
fi

# 4. Verify Model Existence
MODEL_PATH=${ASTHRA_MODEL_PATH:-"yolo26n.pt"}
if [ ! -e "$MODEL_PATH" ]; then
    echo "Error: Model not found at $MODEL_PATH"
    echo "Please run ./deployment/raspberry_pi/setup_model.sh to prepare the production model."
    exit 1
fi
echo "Model verified: $MODEL_PATH"

# 5. Verify Camera Source
CAMERA_SOURCE=${ASTHRA_CAMERA_SOURCE:-0}
echo "Using camera source: $CAMERA_SOURCE"

# 6. Start the system
python3 main.py
