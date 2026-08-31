from app.core.enums.hand_gesture import HandGesture
from app.core.models.hand_gesture_event import HandGestureEvent


def test_hand_gesture_event_stores_gesture():
    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
    )

    assert event.gesture == HandGesture.OPEN


def test_hand_gesture_event_stores_position():
    from app.core.models.point import Point

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=Point(
            x=100.0,
            y=200.0,
        ),
    )

    assert event.position == Point(
        x=100.0,
        y=200.0,
    )


def test_hand_gesture_event_has_default_confidence():
    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
    )

    assert event.confidence == 0.0


def test_hand_gesture_event_stores_confidence():
    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        confidence=0.95,
    )

    assert event.confidence == 0.95


def test_hand_gesture_event_has_timestamp():
    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
    )

    assert event.timestamp is not None


def test_hand_gesture_event_timestamp_is_utc():
    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
    )

    assert event.timestamp.tzinfo is not None
    assert event.timestamp.utcoffset().total_seconds() == 0
