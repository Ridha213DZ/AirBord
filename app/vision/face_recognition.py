from dataclasses import dataclass

from app.core.models.face_identity import FaceIdentity
from app.vision.models.detected_face import DetectedFace


@dataclass
class FaceRecognitionResult:
    face: DetectedFace
    identity: FaceIdentity | None


class FaceRecognition:

    def __init__(
        self,
        encoder,
        matcher,
    ):
        self.encoder = encoder
        self.matcher = matcher

    def recognize(
        self,
        frame,
        faces: list[DetectedFace],
        identities: list[FaceIdentity],
    ) -> list[FaceRecognitionResult]:
        results = []

        for face in faces:
            embedding = self.encoder.encode(
                frame,
                face,
            )

            identity = None

            if embedding is not None:
                identity = self.matcher.match(
                    embedding,
                    identities,
                )

            results.append(
                FaceRecognitionResult(
                    face=face,
                    identity=identity,
                )
            )

        return results
