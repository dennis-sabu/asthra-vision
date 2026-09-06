class EMASmoother:
    """
    Exponential Moving Average (EMA) smoother for reducing jitter in sensor data.
    """
    def __init__(self, alpha=0.2, initial_value=None):
        self.alpha = alpha
        self.value = initial_value

    def update(self, current_value):
        """
        Update the smoothed value using the EMA formula:
        S_t = alpha * X_t + (1 - alpha) * S_{t-1}
        """
        if self.value is None:
            self.value = current_value
            return self.value

        self.value = (self.alpha * current_value) + (1 - self.alpha) * self.value
        return self.value

    def reset(self, initial_value=None):
        self.value = initial_value
