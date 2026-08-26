class OpenCVSFaceBackend:

    def __init__(self, recognizer):
        self.recognizer = recognizer

    def encode(self, frame, face):
        face_box = [
            face.x,
            face.y,
            face.width,
            face.height,
        ]

        aligned_image = self.recognizer.alignCrop(
            frame,
            face_box,
        )

        return self.recognizer.feature(
            aligned_image,
        )
