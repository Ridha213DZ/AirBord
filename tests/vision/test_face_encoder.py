from app.vision.face_encoder import FaceEncoder
from app.vision.models.detected_face import DetectedFace


class FakeFaceEncoder:

    def encode(
        self,
        frame,
        face: DetectedFace,
    ) -> list[float]:
        return [
            0.1,
            0.2,
            0.3,
        ]


def test_face_encoder_accepts_frame_and_detected_face_and_returns_embedding():
    encoder: FaceEncoder = FakeFaceEncoder()

    frame = object()

    face = DetectedFace(
        x=100,
        y=80,
        width=200,
        height=200,
        confidence=0.95,
    )

    embedding = encoder.encode(
        frame,
        face,
    )

    assert isinstance(
        embedding,
        list,
    )

    assert all(
        isinstance(value, float)
        for value in embedding
    )

    assert len(embedding) > 0
