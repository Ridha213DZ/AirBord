import numpy as np

from PySide6.QtWidgets import QApplication

from app.vision.models.detected_face import DetectedFace
from app.ui.camera_preview_window import CameraPreviewWindow


class FakeCameraFrameSource:

    def __init__(self, frame):
        self.frame = frame

    def read(self):
        return self.frame

    def close(self):
        pass


class FakeFaceDetector:

    def __init__(self, faces):
        self.faces = faces
        self.received_frame = None

    def detect(self, frame):
        self.received_frame = frame
        return self.faces


def test_camera_preview_window_sends_frame_to_yunet_detector():
    app = QApplication.instance() or QApplication([])

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    source = FakeCameraFrameSource(
        frame=frame,
    )

    detector = FakeFaceDetector(
        faces=[],
    )

    window = CameraPreviewWindow(
        source=source,
        face_detector=detector,
    )

    window.update_frame()

    assert detector.received_frame is frame


def test_camera_preview_window_sends_detected_faces_to_preview():
    app = QApplication.instance() or QApplication([])

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    face = DetectedFace(
        x=100,
        y=80,
        width=200,
        height=200,
        confidence=0.95,
    )

    source = FakeCameraFrameSource(
        frame=frame,
    )

    detector = FakeFaceDetector(
        faces=[face],
    )

    window = CameraPreviewWindow(
        source=source,
        face_detector=detector,
    )

    window.update_frame()

    assert window.preview.faces == [face]
