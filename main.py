import cv2

from camera.webcam import Webcam
from detection.person_detector import PersonDetector
from tracking.person_tracker import PersonTracker


def main():

    webcam = Webcam()
    detector = PersonDetector()
    tracker = PersonTracker()

    while True:

        success, frame = webcam.read()

        if not success:
            print("Could not read from camera")
            break

        frame_height, frame_width = frame.shape[:2]

        # Detect people
        people = detector.detect(frame)

        # Select person to track
        tracking_data = tracker.select_target(
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

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

        # Target tracking information
        if tracking_data:

            person_center = tracking_data["center"]
            error_x, error_y = tracking_data["error"]

            # Highlight selected target
            x1, y1, x2, y2 = tracking_data["person"]["bbox"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                3
            )

            # Person centre
            cv2.circle(
                frame,
                person_center,
                6,
                (0, 0, 255),
                -1
            )

            # Direction
            if error_x < -50:
                direction = "LOOK LEFT"

            elif error_x > 50:
                direction = "LOOK RIGHT"

            else:
                direction = "CENTER"

            cv2.putText(
                frame,
                f"TARGET: {direction}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"X Error: {error_x}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # Draw line from camera centre to person
            cv2.line(
                frame,
                (frame_center_x, frame_center_y),
                person_center,
                (255, 0, 255),
                2
            )

        else:

            cv2.putText(
                frame,
                "NO PERSON DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        cv2.imshow("ASTHRA Vision - Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    webcam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()