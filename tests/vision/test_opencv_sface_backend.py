import numpy as np

from app.vision.models.detected_face import DetectedFace
from app.vision.backends.opencv_sface_backend import (
    OpenCVSFaceBackend,
)


class FakeSFaceRecognizer:

    def __init__(self):
        self.received_image = None
        self.received_face_box = None
        self.received_aligned_image = None

    def alignCrop(
        self,
        image,
        face_box,
    ):
        self.received_image = image
        self.received_face_box = face_box

        return np.zeros(
            (112, 112, 3),
            dtype=np.uint8,
        )

    def feature(
        self,
        aligned_image,
    ):
        self.received_aligned_image = aligned_image

        return np.array(
            [
                [0.1, 0.2, 0.3],
            ],
            dtype=np.float32,
        )


def test_opencv_sface_backend_extracts_feature():
    recognizer = FakeSFaceRecognizer()

    backend = OpenCVSFaceBackend(
        recognizer=recognizer,
    )

    frame = object()

    face = DetectedFace(
        x=100,
        y=80,
        width=200,
        height=200,
        confidence=0.95,
    )

    embedding = backend.encode(
        frame,
        face,
    )

    assert recognizer.received_image is frame

    assert recognizer.received_face_box == [
        100,
        80,
        200,
        200,
    ]

    assert recognizer.received_aligned_image is not None

    assert isinstance(
        embedding,
        np.ndarray,
    )

    assert embedding.shape == (1, 3)

    np.testing.assert_allclose(
        embedding,
        np.array(
            [
                [0.1, 0.2, 0.3],
            ],
            dtype=np.float32,
        ),
    )
