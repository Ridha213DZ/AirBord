from typing import Protocol

from app.vision.models.detected_face import DetectedFace


class FaceEncoder(Protocol):

    def encode(
        self,
        frame,
        face: DetectedFace,
    ) -> list[float] | None:
        ...