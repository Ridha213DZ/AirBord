from typing import Any

import cv2


class CameraFrameSource:

    def __init__(self, capture: Any):
        self.capture = capture

    @classmethod
    def open(cls, device: int = 0):
        capture = cv2.VideoCapture(device)

        return cls(capture)

    def read(self):
        ok, frame = self.capture.read()

        if not ok:
            return None

        return frame

    def close(self):
        self.capture.release()
