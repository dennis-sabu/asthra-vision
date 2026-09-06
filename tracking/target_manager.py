import time
from config import LOCK_TIMEOUT, DISTANCE_THRESHOLDS

class TargetManager:
    """
    Manages target selection and locking logic to prevent rapid switching
    between multiple detected people.
    """
    def __init__(self):
        self.locked_target_bbox = None
        self.last_seen_time = 0
        self.is_locked = False

    def _calculate_iou(self, boxA, boxB):
        """
        Calculate Intersection over Union (IoU) of two bounding boxes.
        Boxes are in (x1, y1, x2, y2) format.
        """
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB - xA) * max(0, yB - yA)

        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

        iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
        return iou

    def get_target(self, people):
        """
        Selects the best target person based on locking logic.
        """
        current_time = time.time()

        # If no people detected, check if we should release the lock
        if not people:
            if self.is_locked and (current_time - self.last_seen_time > LOCK_TIMEOUT):
                self.is_locked = False
                self.locked_target_bbox = None
            return None

        # Try to find the previously locked target using IoU
        if self.is_locked:
            best_iou = 0
            best_person = None

            for person in people:
                iou = self._calculate_iou(self.locked_target_bbox, person["bbox"])
                if iou > best_iou:
                    best_iou = iou
                    best_person = person

            # Lock threshold: IoU > 0.3 is typically enough to consider it the same person
            if best_person and best_iou > 0.3:
                self.locked_target_bbox = best_person["bbox"]
                self.last_seen_time = current_time
                return best_person

        # No lock or locked target lost: select the largest person as new target
        target = max(
            people,
            key=lambda p: (p["bbox"][2] - p["bbox"][0]) * (p["bbox"][3] - p["bbox"][1])
        )

        self.is_locked = True
        self.locked_target_bbox = target["bbox"]
        self.last_seen_time = current_time
        return target

    def estimate_distance(self, bbox, frame_width, frame_height):
        """
        Estimate distance based on bounding box area relative to frame area.
        """
        x1, y1, x2, y2 = bbox
        bbox_area = (x2 - x1) * (y2 - y1)
        frame_area = frame_width * frame_height
        ratio = bbox_area / frame_area

        if ratio >= DISTANCE_THRESHOLDS["CLOSE"]:
            return "CLOSE"
        elif ratio >= DISTANCE_THRESHOLDS["MEDIUM"]:
            return "MEDIUM"
        else:
            return "FAR"
