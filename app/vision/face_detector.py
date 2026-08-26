from app.vision.models.detected_face import DetectedFace


class FaceDetector:

    def __init__(self, backend):
        self.backend = backend

    def detect(self, frame) -> list[DetectedFace]:
        detections = self.backend.detect(frame)

        return [
            DetectedFace(
                x=int(detection[0]),
                y=int(detection[1]),
                width=int(detection[2]),
                height=int(detection[3]),
                confidence=float(detection[-1]),
            )
            for detection in detections
        ]
