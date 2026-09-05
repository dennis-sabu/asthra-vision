from ultralytics import YOLO


class PersonDetector:
    def __init__(self, model_path="yolo26n.pt", confidence=0.5):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):
        results = self.model(
            frame,
            classes=[0],  # Person class only
            conf=self.confidence,
            verbose=False
        )

        people = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])

                people.append({
                    "bbox": (
                        int(x1),
                        int(y1),
                        int(x2),
                        int(y2)
                    ),
                    "confidence": confidence
                })

        return people