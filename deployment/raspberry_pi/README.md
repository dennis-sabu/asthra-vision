# Raspberry Pi 4 Deployment Guide

This directory contains the tools and scripts necessary to deploy ASTHRA Vision on a Raspberry Pi 4 Model B.

## Prerequisites

- **Hardware**: Raspberry Pi 4 Model B (4GB or 8GB RAM recommended).
- **OS**: Raspberry Pi OS 64-bit.
- **Camera**: USB Webcam or ESP32-CAM Wi-Fi stream.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd asthra-vision
   ```

2. **Run the installation script**:
   ```bash
   chmod +x deployment/raspberry_pi/install.sh
   ./deployment/raspberry_pi/install.sh
   ```
   This script will install system dependencies and create a Python virtual environment.

## Configuration

You can configure the system without modifying the code using environment variables.

### Camera Source
- **USB Webcam**: Set `ASTHRA_CAMERA_SOURCE` to the index (e.g., `0`).
- **ESP32-CAM**: Set `ASTHRA_CAMERA_SOURCE` to the HTTP stream URL (e.g., `http://192.168.1.100/stream`).

### Model and Performance
- **Model Path**: Set `ASTHRA_MODEL_PATH` to point to your model file (e.g., `yolov8n.pt`).
- **NCNN Optimization**: For maximum performance on Pi 4, export your model to NCNN format:
  ```bash
  # In the virtual environment
  python3 -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); model.export(format='ncnn')"
  ```
  Then set `ASTHRA_MODEL_PATH` to the path of the exported NCNN folder.

## Running ASTHRA Vision

To start the system, use the run script:
```bash
chmod +x deployment/raspberry_pi/run.sh
./deployment/raspberry_pi/run.sh
```

## Troubleshooting

- **Permission Denied**: Ensure you have given execution permissions to the scripts using `chmod +x`.
- **Camera Not Found**: Check your USB connection or ensure the ESP32-CAM is reachable on the network.
- **Slow FPS**: Ensure you are using the Nano version of YOLO (`yolov8n`) and consider exporting to NCNN.
