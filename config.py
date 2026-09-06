# ASTHRA Vision Configuration
import os

class Config:
    # Camera Settings
    CAMERA_SOURCE = os.getenv("ASTHRA_CAMERA_SOURCE", 0)  # USB index or HTTP URL
    CAMERA_WIDTH = int(os.getenv("ASTHRA_CAMERA_WIDTH", 640))
    CAMERA_HEIGHT = int(os.getenv("ASTHRA_CAMERA_HEIGHT", 480))

    # Model Settings
    YOLO_MODEL_PATH = os.getenv("ASTHRA_MODEL_PATH", "yolo26n.pt")
    MODEL_TYPE = os.getenv("ASTHRA_MODEL_TYPE", "standard")  # "standard" or "ncnn"
    PERSON_CONFIDENCE = float(os.getenv("ASTHRA_CONFIDENCE", 0.5))

    # Target Locking
    LOCK_TIMEOUT = float(os.getenv("ASTHRA_LOCK_TIMEOUT", 2.0))  # Seconds to wait before releasing target lock

    # Position Smoothing
    EMA_ALPHA = float(os.getenv("ASTHRA_EMA_ALPHA", 0.2))  # Smoothing factor (lower = more smooth, higher = more responsive)

    # Virtual Neck
    YAW_MAX = float(os.getenv("ASTHRA_YAW_MAX", 40.0))  # Maximum yaw angle in degrees
    YAW_MIN = float(os.getenv("ASTHRA_YAW_MIN", -40.0))  # Minimum yaw angle in degrees

    # Distance Estimation (Bounding Box Area / Frame Area)
    DISTANCE_THRESHOLDS = {
        "CLOSE": 0.15,   # > 15% of frame
        "MEDIUM": 0.05,  # 5% - 15% of frame
        "FAR": 0.0       # < 5% of frame
    }

    # Position Zone Thresholds (Normalized X)
    ZONE_THRESHOLDS = {
        "LEFT": 0.33,    # < 33%
        "RIGHT": 0.66    # > 66%
    }

# --- Backward Compatibility Layer ---
# These constants allow the rest of the app to continue working without changes
LOCK_TIMEOUT = Config.LOCK_TIMEOUT
EMA_ALPHA = Config.EMA_ALPHA
YAW_MAX = Config.YAW_MAX
YAW_MIN = Config.YAW_MIN
DISTANCE_THRESHOLDS = Config.DISTANCE_THRESHOLDS
ZONE_THRESHOLDS = Config.ZONE_THRESHOLDS
PERSON_CONFIDENCE = Config.PERSON_CONFIDENCE
YOLO_MODEL_PATH = Config.YOLO_MODEL_PATH

