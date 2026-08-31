from app.core.enums.hand_gesture import HandGesture


def test_hand_gesture_defines_open_and_fist_states():
    assert HandGesture.OPEN.value == "open"
    assert HandGesture.FIST.value == "fist"
