from app.vision.models.detected_face import DetectedFace


class FaceSelector:

    def select(
        self,
        faces: list[DetectedFace],
        target_region: tuple[int, int, int, int] | None = None,
    ) -> DetectedFace | None:

        if not faces:
            return None

        if target_region is not None:
            x, y, width, height = target_region

            faces = [
                face
                for face in faces
                if (
                    face.x >= x
                    and face.y >= y
                    and face.x + face.width <= x + width
                    and face.y + face.height <= y + height
                )
            ]

            if not faces:
                return None

        return max(
            faces,
            key=lambda face: face.width * face.height,
        )