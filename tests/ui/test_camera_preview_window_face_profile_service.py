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

    def __init__(self, face):
        self.face = face

    def detect(self, frame):
        return [self.face]


class FakeFaceProfileService:

    def __init__(self, results):
        self.results = results
        self.received_frame = None
        self.received_faces = None

    def process(self, frame, faces):
        self.received_frame = frame
        self.received_faces = faces

        return self.results


def test_camera_preview_window_uses_face_profile_service():
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

    expected_results = [object()]

    face_profile_service = FakeFaceProfileService(
        results=expected_results,
    )

    window = CameraPreviewWindow(
        source=FakeCameraFrameSource(frame),
        face_detector=FakeFaceDetector(face),
        face_profile_service=face_profile_service,
    )

    window.update_frame()

    assert face_profile_service.received_frame is frame
    assert face_profile_service.received_faces == [face]
    assert window.preview.recognition_results == expected_results
