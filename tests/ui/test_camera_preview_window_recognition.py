import numpy as np
from PySide6.QtWidgets import QApplication

from app.core.models.face_identity import FaceIdentity
from app.ui.camera_preview_window import CameraPreviewWindow
from app.vision.models.detected_face import DetectedFace


class FakeCameraFrameSource:

    def __init__(self, frame):
        self.frame = frame

    def read(self):
        return self.frame

    def close(self):
        pass


class FakeFaceRecognition:

    def __init__(self, result):
        self.result = result
        self.received_frame = None
        self.received_faces = None
        self.received_identities = None

    def recognize(self, frame, faces, identities):
        self.received_frame = frame
        self.received_faces = faces
        self.received_identities = identities

        return self.result


def test_camera_preview_window_sends_detected_faces_to_recognition():
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

    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    class FaceDetector:

        def detect(self, received_frame):
            assert received_frame is frame
            return [face]

    recognition_result = object()

    recognition = FakeFaceRecognition(
        result=[recognition_result],
    )

    window = CameraPreviewWindow(
        source=FakeCameraFrameSource(frame),
        face_detector=FaceDetector(),
        face_recognition=recognition,
        identities=[identity],
    )

    window.update_frame()

    assert recognition.received_frame is frame
    assert recognition.received_faces == [face]
    assert recognition.received_identities == [identity]


def test_camera_preview_window_sends_recognition_results_to_preview():
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

    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    class FaceDetector:

        def detect(self, received_frame):
            return [face]

    class FakeRecognition:

        def recognize(self, frame, faces, identities):
            return [
                {
                    "face": face,
                    "identity": identity,
                }
            ]

    window = CameraPreviewWindow(
        source=FakeCameraFrameSource(frame),
        face_detector=FaceDetector(),
        face_recognition=FakeRecognition(),
        identities=[identity],
    )

    window.update_frame()

    assert window.preview.recognition_results == [
        {
            "face": face,
            "identity": identity,
        }
    ]
