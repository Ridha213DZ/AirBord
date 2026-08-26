class FacePipeline:
    def __init__(
        self,
        detector,
        selector,
    ):
        self.detector = detector
        self.selector = selector

    def process(
        self,
        frame,
        target_region=None,
    ):
        faces = self.detector.detect(frame)

        if not faces:
            return None

        return self.selector.select(
            faces,
            target_region=target_region,
        )
