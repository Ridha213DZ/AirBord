from app.core.enums.hand_gesture import HandGesture
from app.core.models.hand_gesture_event import HandGestureEvent
from app.core.models.point import Point
from app.vision.hand_gesture_recognizer import (
    HandGestureRecognizer,
)


def test_hand_gesture_recognizer_maps_open_palm_to_open():
    recognizer = HandGestureRecognizer()

    result = recognizer.recognize(
        gesture_name="Open_Palm",
        confidence=0.95,
        position=Point(
            x=100.0,
            y=200.0,
        ),
    )

    assert isinstance(
        result,
        HandGestureEvent,
    )

    assert result.gesture == HandGesture.OPEN

    assert result.position == Point(
        x=100.0,
        y=200.0,
    )

    assert result.confidence == 0.95


def test_hand_gesture_recognizer_rejects_unknown_gesture():
    recognizer = HandGestureRecognizer()

    try:
        recognizer.recognize(
            gesture_name="Unknown_Gesture",
            confidence=0.95,
            position=Point(
                x=100.0,
                y=200.0,
            ),
        )
        assert False
    except ValueError:
        pass


def test_hand_gesture_recognizer_rejects_low_confidence_gesture():
    recognizer = HandGestureRecognizer()

    result = recognizer.recognize(
        gesture_name="Open_Palm",
        confidence=0.35,
        position=Point(
            x=100.0,
            y=200.0,
        ),
    )

    assert result is None


def test_hand_gesture_recognizer_accepts_confidence_at_threshold():
    recognizer = HandGestureRecognizer()

    result = recognizer.recognize(
        gesture_name="Open_Palm",
        confidence=0.5,
        position=Point(
            x=100.0,
            y=200.0,
        ),
    )

    assert result is not None
    assert result.gesture == HandGesture.OPEN
    assert result.confidence == 0.5


def test_hand_gesture_recognizer_rejects_invalid_confidence():
    recognizer = HandGestureRecognizer()

    for confidence in (-0.1, 1.1):
        try:
            recognizer.recognize(
                gesture_name="Open_Palm",
                confidence=confidence,
                position=Point(
                    x=100.0,
                    y=200.0,
                ),
            )
            assert False
        except ValueError:
            pass


def test_hand_gesture_recognizer_maps_mediapipe_result():
    class Category:
        category_name = "Open_Palm"
        score = 0.95

    class Landmark:
        x = 0.25
        y = 0.5

    class MediaPipeResult:
        gestures = [
            [Category()]
        ]
        hand_landmarks = [
            [Landmark()]
        ]

    recognizer = HandGestureRecognizer()

    result = recognizer.recognize_mediapipe(
        MediaPipeResult()
    )

    assert isinstance(
        result,
        HandGestureEvent,
    )

    assert result.gesture == HandGesture.OPEN

    assert result.position == Point(
        x=0.25,
        y=0.5,
    )

    assert result.confidence == 0.95


def test_hand_gesture_recognizer_returns_none_without_gesture_category():
    class MediaPipeResult:
        gestures = [[]]
        hand_landmarks = [
            [type("Landmark", (), {"x": 0.25, "y": 0.5})()]
        ]

    recognizer = HandGestureRecognizer()

    result = recognizer.recognize_mediapipe(
        MediaPipeResult()
    )

    assert result is None


def test_hand_gesture_recognizer_returns_none_without_hand_landmarks():
    class Category:
        category_name = "Open_Palm"
        score = 0.95

    class MediaPipeResult:
        gestures = [
            [Category()]
        ]
        hand_landmarks = [[]]

    recognizer = HandGestureRecognizer()

    result = recognizer.recognize_mediapipe(
        MediaPipeResult()
    )

    assert result is None
