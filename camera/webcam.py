import cv2
from config import Config


class Webcam:
    def __init__(self, source=None, width=None, height=None):
        # Use provided source or fallback to config
        self.source = source if source is not None else Config.CAMERA_SOURCE
        self.width = width if width is not None else Config.CAMERA_WIDTH
        self.height = height if height is not None else Config.CAMERA_HEIGHT

        # source can be an integer (USB index) or a string (HTTP URL)
        # If it's a string but looks like an integer, convert it
        if isinstance(self.source, str) and self.source.isdigit():
            self.source = int(self.source)

        self.camera = cv2.VideoCapture(self.source)

        # Set resolution if possible
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        success, frame = self.camera.read()
        return success, frame

    def release(self):
        self.camera.release()