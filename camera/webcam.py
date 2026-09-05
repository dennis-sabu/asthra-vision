import cv2


class Webcam:
    def __init__(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)

    def read(self):
        success, frame = self.camera.read()
        return success, frame

    def release(self):
        self.camera.release()