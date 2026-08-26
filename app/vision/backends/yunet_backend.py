class YuNetBackend:

    def __init__(self, detector):
        self.detector = detector

    def detect(self, frame):
        _, detections = self.detector.detect(frame)

        if detections is None:
            return []

        return detections.tolist()
