#!/bin/bash

# ASTHRA Vision - Raspberry Pi Model Setup Script
# This script exports the YOLO26n model to NCNN format for production inference.

set -e

echo "--------------------------------------------------"
echo "ASTHRA Vision: Model Setup (YOLO26n -> NCNN)"
echo "--------------------------------------------------"

# 1. Locate project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# 2. Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Please run ./deployment/raspberry_pi/install.sh first."
    exit 1
fi

# 3. Define model names and paths
INPUT_MODEL="yolo26n.pt"
EXPORT_DIR="models/production/yolo26n_ncnn_model"

# 4. Ensure input model exists
if [ ! -f "$INPUT_MODEL" ]; then
    echo "Model $INPUT_MODEL not found in root directory."
    echo "Attempting to download default yolov8n.pt as fallback..."
    wget -O "$INPUT_MODEL" https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt || {
        echo "Error: Failed to download model. Please place $INPUT_MODEL in the root directory."
        exit 1
    }
fi

# 5. Export model to NCNN
echo "Exporting $INPUT_MODEL to NCNN format..."
python3 -c "from ultralytics import YOLO; model = YOLO('$INPUT_MODEL'); model.export(format='ncnn')"

# 6. Organize model files
# Ultralytics exports NCNN models into a directory named <model_name>_ncnn_model
EXPECTED_EXPORT_DIR="${INPUT_MODEL%.*}_ncnn_model"

if [ -d "$EXPECTED_EXPORT_DIR" ]; then
    echo "Export successful. Moving model to production directory..."
    mkdir -p models/production
    rm -rf "$EXPORT_DIR"
    mv "$EXPECTED_EXPORT_DIR" "$EXPORT_DIR"
    echo "Model placed at: $EXPORT_DIR"
else
    echo "Error: Export directory $EXPECTED_EXPORT_DIR not found."
    exit 1
fi

echo "--------------------------------------------------"
echo "SUCCESS: YOLO26n NCNN model is ready for production!"
echo "Set ASTHRA_MODEL_PATH=$EXPORT_DIR in your environment."
echo "--------------------------------------------------"
