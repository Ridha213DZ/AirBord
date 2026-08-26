import numpy as np

from app.vision.models.detected_face import DetectedFace
from app.vision.opencv_face_encoder import OpenCVFaceEncoder


class FakeSFaceBackend:

    def align_crop(
        self,
        frame,
        face,
    ):
        return np.zeros(
            (112, 112, 3),
            dtype=np.uint8,
        )

    def feature(
        self,
        aligned_face,
    ):
        return np.array(
            [
                [0.1, 0.2, 0.3],
            ],
            dtype=np.float32,
        )


def test_opencv_face_encoder_returns_embedding():
    encoder = OpenCVFaceEncoder(
        backend=FakeSFaceBackend(),
    )

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
