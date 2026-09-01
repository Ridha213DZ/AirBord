import numpy as np

from app.core.enums.hand_gesture import HandGesture
from app.core.models.hand_gesture_event import HandGestureEvent
from app.vision.hand_gesture_recognizer import (
    HandGestureRecognizer,
)
from app.vision.mediapipe_gesture_detector import (
    MediaPipeGestureDetector,
)


def test_mediapipe_gesture_detection_result_is_recognized_as_hand_gesture_event():
    class FakeCategory:

        def __init__(
            self,
            category_name,
            score,
        ):
            self.category_name = category_name
            self.score = score

    class FakeLandmark:

        def __init__(
            self,
            x,
            y,
        ):
            self.x = x
            self.y = y

    class FakeMediaPipeResult:

        gestures = [
            [
                FakeCategory(
                    category_name="Open_Palm",
                    score=0.95,
                )
            ]
        ]

        hand_landmarks = [
            [
                FakeLandmark(
                    x=0.4,
                    y=0.6,
                )
            ]
        ]

    class FakeRecognizer:

        def recognize(self, image):
            return FakeMediaPipeResult()

    detector = MediaPipeGestureDetector(
        recognizer=FakeRecognizer(),
    )

    gesture_recognizer = HandGestureRecognizer()

    frame = np.zeros(
        (100, 200, 3),
        dtype=np.uint8,
    )

    mediapipe_result = detector.detect(frame)

    event = gesture_recognizer.recognize_mediapipe(
        mediapipe_result
    )

    assert isinstance(
        event,
        HandGestureEvent,
    )

    assert event.gesture == HandGesture.OPEN
    assert event.confidence == 0.95
    assert event.position.x == 0.4
    assert event.position.y == 0.6
