from app.vision.models.detected_face import DetectedFace


class OpenCVFaceEncoder:

    def __init__(self, backend):
        self.backend = backend

    def encode(
        self,
        frame,
        face: DetectedFace,
    ) -> list[float]:
        aligned_face = self.backend.align_crop(
            frame,
            face,
        )

        embedding = self.backend.feature(
            aligned_face,
        )

        return embedding.flatten().tolist()
