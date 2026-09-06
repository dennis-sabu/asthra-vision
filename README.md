# ASTHRA Vision

ASTHRA Vision is the computer vision subsystem for the ASTHRA welcome robot. It currently runs on a laptop webcam and uses Ultralytics YOLO to detect people, select a target, and calculate the target's position relative to the camera frame.

The project is designed to support both Windows Laptop development and Raspberry Pi 4 deployment.

## Current Features

- Captures live video from a laptop webcam, USB webcam, or ESP32-CAM Wi-Fi stream.
- Detects people only using the YOLO person class.
- Processes multiple detected people in each frame.
- Selects the largest detected person as the current target.
- Calculates the target centre and its horizontal and vertical error from the frame centre.
- Displays left, centre, and right tracking status in real time.
- Draws all detections, the selected target, centres, and tracking information on the video feed.

## Project Structure

```text
asthra-vision/
├── main.py                         # Application entry point
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── README.md
├── camera/
│   └── webcam.py                   # Camera capture interface (USB & HTTP)
├── detection/
│   └── person_detector.py          # YOLO person detection
├── tracking/
│   └── person_tracker.py           # Target selection and position tracking
├── control/                        # Robot control logic
├── utils/                          # Shared utilities
└── deployment/                     # Environment-specific deployment scripts
    └── raspberry_pi/                # Raspberry Pi 4 installation and run tools
```

The YOLO model file is downloaded locally and is intentionally excluded from Git. Source code, configuration, documentation, and dependency files remain available for GitHub.

## Laptop Development

### Requirements

- Python 3.9 or newer
- A working laptop webcam
- Windows, macOS, or Linux

### Installation

From the project directory, create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Download or place the YOLO model file expected by the detector in the project root:

```text
yolo26n.pt
```

Run the vision system:

```bash
python main.py
```

The webcam window shows the live detections and tracking direction. Press `q` to stop the application.

## Raspberry Pi 4 Deployment

This system is optimized for Raspberry Pi OS (64-bit).

### Installation

1. Clone the repository and enter the directory:
   ```bash
   git clone <repository-url>
   cd asthra-vision
   ```

2. Run the automated installation script:
   ```bash
   chmod +x deployment/raspberry_pi/install.sh
   ./deployment/raspberry_pi/install.sh
   ```

### Configuration

You can configure the system using environment variables without editing the code:

- **Camera Source**: `ASTHRA_CAMERA_SOURCE` (e.g., `0` for USB or `http://...` for ESP32-CAM).
- **Resolution**: `ASTHRA_CAMERA_WIDTH` and `ASTHRA_CAMERA_HEIGHT`.
- **Model Path**: `ASTHRA_MODEL_PATH` (e.g., `yolov8n.pt`).

### Execution

To start ASTHRA Vision on the Pi:
```bash
chmod +x deployment/raspberry_pi/run.sh
./deployment/raspberry_pi/run.sh
```

For detailed Pi-specific setup, including NCNN model optimization, see [deployment/raspberry_pi/README.md](deployment/raspberry_pi/README.md).

## Future Hardware Integration

Hardware integration is planned but is not part of the current implementation. The intended roadmap is:

1. Laptop webcam development and testing.
2. Person detection and target tracking.
3. Virtual neck control and control interface design.
4. Raspberry Pi 4 deployment.
5. ESP32-CAM video stream integration.
6. Real servo control.
7. ASTHRA welcome robot behavior.

## Notes

- The default camera is device `0`.
- The detector currently uses the person class only.
- The largest detected person is selected as the tracking target.
- Model files, virtual environments, secrets, logs, caches, and build artifacts are excluded through `.gitignore`.
