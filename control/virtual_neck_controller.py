from config import YAW_MAX, YAW_MIN

class VirtualNeckController:
    """
    Calculates a virtual yaw angle based on the person's normalized position.
    """
    def calculate_yaw(self, normalized_x):
        """
        Maps normalized_x (0.0 to 1.0) to yaw angle (YAW_MIN to YAW_MAX).
        0.0 (Far Left) -> YAW_MIN
        0.5 (Center) -> 0.0
        1.0 (Far Right) -> YAW_MAX
        """
        # Linear mapping: (normalized_x - 0.5) * (Total Range)
        # Total Range = YAW_MAX - YAW_MIN (e.g., 40 - (-40) = 80)
        yaw = (normalized_x - 0.5) * (YAW_MAX - YAW_MIN)

        # Clamp the value to ensure it stays within range
        return max(YAW_MIN, min(YAW_MAX, yaw))
