from app.core.enums.hand_gesture import HandGesture
from app.core.models.hand_gesture_event import HandGestureEvent
from app.core.models.point import Point
from app.vision.hand_gesture_pipeline import (
    HandGesturePipeline,
)


def test_hand_gesture_pipeline_returns_recognized_hand_gesture_event():
    class FakeDetector:

        def __init__(self):
            self.received_frame = None

        def detect(self, frame):
            self.received_frame = frame
            return "mediapipe result"

    class FakeGestureRecognizer:

        def __init__(self):
            self.received_result = None

        def recognize_mediapipe(self, result):
            self.received_result = result

            return HandGestureEvent(
                gesture=HandGesture.OPEN,
                position=Point(
                    x=0.4,
                    y=0.6,
                ),
                confidence=0.95,
            )

    detector = FakeDetector()

    gesture_recognizer = FakeGestureRecognizer()

    pipeline = HandGesturePipeline(
        detector=detector,
        gesture_recognizer=gesture_recognizer,
    )

    frame = object()

    event = pipeline.process(frame)

    assert detector.received_frame is frame

    assert (
        gesture_recognizer.received_result
        == "mediapipe result"
    )

    assert isinstance(
        event,
        HandGestureEvent,
    )

    assert event.gesture == HandGesture.OPEN
    assert event.position == Point(
        x=0.4,
        y=0.6,
    )
    assert event.confidence == 0.95


def test_hand_gesture_pipeline_returns_none_when_gesture_is_not_recognized():
    class FakeDetector:

        def detect(self, frame):
            return "mediapipe result"

    class FakeGestureRecognizer:

        def recognize_mediapipe(self, result):
            return None

    pipeline = HandGesturePipeline(
        detector=FakeDetector(),
        gesture_recognizer=FakeGestureRecognizer(),
    )

    event = pipeline.process(
        object()
    )

    assert event is None
