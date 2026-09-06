import cv2

from camera.webcam import Webcam
from detection.person_detector import PersonDetector
from tracking.person_tracker import PersonTracker
from config import PERSON_CONFIDENCE, YOLO_MODEL_PATH

def main():
    webcam = Webcam()
    detector = PersonDetector(model_path=YOLO_MODEL_PATH, confidence=PERSON_CONFIDENCE)
    tracker = PersonTracker()

    while True:
        success, frame = webcam.read()

        if not success:
            print("Could not read from camera")
            break

        frame_height, frame_width = frame.shape[:2]

        # Detect people
        people = detector.detect(frame)

        # Update tracking state
        tracking_data = tracker.update(
            people,
            frame_width,
            frame_height
        )

        # Draw camera centre
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2

        cv2.drawMarker(
            frame,
            (frame_center_x, frame_center_y),
            (255, 255, 0),
            cv2.MARKER_CROSS,
            25,
            2
        )

        # Draw all detected people
        for person in people:
            x1, y1, x2, y2 = person["bbox"]
            conf = person["confidence"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                f"{conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

        # Target tracking information
        if tracking_data["target"]:
            target_person = tracking_data["target"]
            person_center = tracking_data["person_center"]

            # Highlight selected target
            x1, y1, x2, y2 = target_person["bbox"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                3
            )
            cv2.putText(
                frame,
                "TARGET",
                (x1, y1 - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            # Person centre
            cv2.circle(
                frame,
                person_center,
                6,
                (0, 0, 255),
                -1
            )

            # Draw line from camera centre to person
            cv2.line(
                frame,
                (frame_center_x, frame_center_y),
                person_center,
                (255, 0, 255),
                2
            )

        # HUD Visualization
        # Background for HUD
        cv2.rectangle(
            frame,
            (0, 0),
            (350, 220),
            (0, 0, 0),
            -1
        )

        # HUD text transparency/overlay
        cv2.rectangle(
            frame,
            (0, 0),
            (350, 220),
            (0, 0, 0),
            1
        )

        # Target Status
        status_color = (0, 255, 0) if tracking_data["is_locked"] else (0, 0, 255)
        status_text = "LOCKED" if tracking_data["is_locked"] else "SEARCHING"

        if not tracking_data["target"]:
            status_text = "NO TARGET"
            status_color = (0, 0, 255)

        cv2.putText(
            frame,
            f"STATUS: {status_text}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            status_color,
            2
        )

        # People Count
        cv2.putText(
            frame,
            f"People Detected: {tracking_data['people_count']}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        # Position Zone
        cv2.putText(
            frame,
            f"Zone: {tracking_data['zone']}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        # Normalized X
        cv2.putText(
            frame,
            f"Normalized X: {tracking_data['smoothed_x']:.3f}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        # Distance Estimation
        cv2.putText(
            frame,
            f"Distance: {tracking_data['distance']}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        # Virtual Neck Angle
        cv2.putText(
            frame,
            f"Neck Yaw: {tracking_data['yaw']:.1f} deg",
            (20, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.imshow("ASTHRA Vision - Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    webcam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
