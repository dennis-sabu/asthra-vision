class PersonTracker:
    def __init__(self):
        pass

    def select_target(self, people, frame_width, frame_height):

        # No people detected
        if not people:
            return None

        # Select the largest detected person
        target = max(
            people,
            key=lambda person: (
                person["bbox"][2] - person["bbox"][0]
            ) * (
                person["bbox"][3] - person["bbox"][1]
            )
        )

        x1, y1, x2, y2 = target["bbox"]

        # Calculate centre of the person
        person_center_x = (x1 + x2) // 2
        person_center_y = (y1 + y2) // 2

        # Calculate centre of camera frame
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2

        # Position difference
        error_x = person_center_x - frame_center_x
        error_y = person_center_y - frame_center_y

        return {
            "person": target,
            "center": (person_center_x, person_center_y),
            "error": (error_x, error_y),
            "frame_center": (frame_center_x, frame_center_y)
        }