import numpy as np

from PySide6.QtWidgets import QApplication

from app.ui.camera_preview_window import CameraPreviewWindow
from app.vision.models.detected_face import DetectedFace


class FakeCameraFrameSource:

    def __init__(self, frame):
        self.frame = frame

    def read(self):
        return self.frame

    def close(self):
        pass


class FakeFaceDetector:

    def __init__(self):
        self.received_frame = None

    def detect(self, frame):
        self.received_frame = frame

        return [
            DetectedFace(
                x=100,
                y=80,
                width=200,
                height=200,
                confidence=0.95,
            )
        ]


def test_camera_preview_window_sends_frame_to_face_detector():
    app = QApplication.instance() or QApplication([])

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    source = FakeCameraFrameSource(
        frame=frame,
    )

    detector = FakeFaceDetector()

    window = CameraPreviewWindow(
        source=source,
        face_detector=detector,
    )

    window.update_frame()

    assert detector.received_frame is frame
