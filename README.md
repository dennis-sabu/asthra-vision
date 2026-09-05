# ASTHRA Vision

ASTHRA Vision is the computer vision subsystem for the ASTHRA welcome robot. It currently runs on a laptop webcam and uses Ultralytics YOLO to detect people, select a target, and calculate the target's position relative to the camera frame.

The project is being developed in stages so the laptop vision system can later provide the input for a Raspberry Pi 4 and an ESP32-based robot.

## Current Features

- Captures live video from a laptop webcam using OpenCV.
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
├── requirements.txt                # Python dependencies
├── README.md
├── camera/
│   └── webcam.py                   # Webcam capture interface
├── detection/
│   └── person_detector.py          # YOLO person detection
├── tracking/
│   └── person_tracker.py           # Target selection and position tracking
├── control/                        # Reserved for future robot control
└── utils/                          # Reserved for shared utilities
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

## Future Hardware Integration

Hardware integration is planned but is not part of the current implementation. The intended roadmap is:

1. Laptop webcam development and testing.
2. Person detection and target tracking.
3. Virtual neck control and control interface design.
4. Raspberry Pi 4 deployment.
5. ESP32-CAM video stream integration.
6. Real servo control.
7. ASTHRA welcome robot behavior.

Raspberry Pi, ESP32-CAM, servo, and robot control code will be added in later stages. No hardware is required to run the current laptop development system.

## Notes

- The default camera is device `0`.
- The detector currently uses the person class only.
- The largest detected person is selected as the tracking target.
- Model files, virtual environments, secrets, logs, caches, and build artifacts are excluded through `.gitignore`.
