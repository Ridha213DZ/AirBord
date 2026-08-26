from math import sqrt

from app.core.models.face_identity import FaceIdentity


class FaceMatcher:

    def __init__(
        self,
        threshold: float = 0.5,
    ):
        self.threshold = threshold

    def match(
        self,
        embedding: list[float],
        identities: list[FaceIdentity],
    ) -> FaceIdentity | None:
        best_identity = None
        best_distance = None

        for identity in identities:
            if not identity.embedding:
                continue

            distance = sqrt(
                sum(
                    (a - b) ** 2
                    for a, b in zip(
                        embedding,
                        identity.embedding,
                    )
                )
            )

            if (
                best_distance is None
                or distance < best_distance
            ):
                best_distance = distance
                best_identity = identity

        if (
            best_identity is None
            or best_distance is None
            or best_distance > self.threshold
        ):
            return None

        return best_identity
