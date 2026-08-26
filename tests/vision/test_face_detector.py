from app.vision.face_detector import FaceDetector
from app.vision.models.detected_face import DetectedFace


class FakeYuNetBackend:

    def detect(self, frame):
        return [
            [
                100.0,
                80.0,
                200.0,
                200.0,
                140.0,
                160.0,
                0.95,
            ]
        ]


def test_face_detector_converts_backend_detection_to_detected_face():
    detector = FaceDetector(
        backend=FakeYuNetBackend(),
    )

    frame = object()

    faces = detector.detect(frame)

    assert len(faces) == 1

    face = faces[0]

    assert isinstance(
        face,
        DetectedFace,
    )

    assert face.x == 100
    assert face.y == 80
    assert face.width == 200
    assert face.height == 200
    assert face.confidence == 0.95
