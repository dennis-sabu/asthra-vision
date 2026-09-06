from config import EMA_ALPHA, ZONE_THRESHOLDS
from utils.smoothing import EMASmoother
from tracking.target_manager import TargetManager
from control.virtual_neck_controller import VirtualNeckController

class PersonTracker:
    def __init__(self):
        self.target_manager = TargetManager()
        self.neck_controller = VirtualNeckController()

        # Smoothers for normalized coordinates
        self.smoother_x = EMASmoother(alpha=EMA_ALPHA)
        self.smoother_y = EMASmoother(alpha=EMA_ALPHA)

    def update(self, people, frame_width, frame_height):
        """
        Processes detected people and updates the target state.
        Returns a comprehensive tracking result.
        """
        # 1. Target Selection and Locking
        target = self.target_manager.get_target(people)

        if target is None:
            # Reset smoothers when no target is available
            self.smoother_x.reset()
            self.smoother_y.reset()

            return {
                "target": None,
                "is_locked": False,
                "normalized_x": 0.5,
                "normalized_y": 0.5,
                "smoothed_x": 0.5,
                "smoothed_y": 0.5,
                "yaw": 0.0,
                "distance": "N/A",
                "zone": "CENTER",
                "people_count": len(people)
            }

        # 2. Position Calculation
        x1, y1, x2, y2 = target["bbox"]

        # Person center
        person_center_x = x1 + (x2 - x1) / 2
        person_center_y = y1 + (y2 - y1) / 2

        # Normalized position
        normalized_x = person_center_x / frame_width
        normalized_y = person_center_y / frame_height

        # 3. Position Smoothing
        smoothed_x = self.smoother_x.update(normalized_x)
        smoothed_y = self.smoother_y.update(normalized_y)

        # 4. Virtual Neck Angle Calculation
        yaw = self.neck_controller.calculate_yaw(smoothed_x)

        # 5. Distance Estimation
        distance = self.target_manager.estimate_distance(target["bbox"], frame_width, frame_height)

        # 6. Zone Classification
        if smoothed_x < ZONE_THRESHOLDS["LEFT"]:
            zone = "LEFT"
        elif smoothed_x > ZONE_THRESHOLDS["RIGHT"]:
            zone = "RIGHT"
        else:
            zone = "CENTER"

        return {
            "target": target,
            "is_locked": self.target_manager.is_locked,
            "normalized_x": normalized_x,
            "normalized_y": normalized_y,
            "smoothed_x": smoothed_x,
            "smoothed_y": smoothed_y,
            "person_center": (int(person_center_x), int(person_center_y)),
            "yaw": yaw,
            "distance": distance,
            "zone": zone,
            "people_count": len(people)
        }
