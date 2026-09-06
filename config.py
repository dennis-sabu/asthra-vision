# ASTHRA Vision Configuration

# Target Locking
LOCK_TIMEOUT = 2.0  # Seconds to wait before releasing target lock

# Position Smoothing
EMA_ALPHA = 0.2     # Smoothing factor (lower = more smooth, higher = more responsive)

# Virtual Neck
YAW_MAX = 40.0     # Maximum yaw angle in degrees
YAW_MIN = -40.0    # Minimum yaw angle in degrees

# Distance Estimation (Bounding Box Area / Frame Area)
# These values are estimates and may need tuning
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

# Detection
PERSON_CONFIDENCE = 0.5
YOLO_MODEL_PATH = "yolo26n.pt"
