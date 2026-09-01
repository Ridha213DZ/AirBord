class HandGesturePipeline:

    def __init__(
        self,
        detector,
        gesture_recognizer,
    ):
        self.detector = detector
        self.gesture_recognizer = gesture_recognizer

    def process(
        self,
        frame,
    ):
        result = self.detector.detect(
            frame
        )

        return self.gesture_recognizer.recognize_mediapipe(
            result
        )
