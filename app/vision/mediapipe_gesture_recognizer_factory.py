import mediapipe as mp

from mediapipe.tasks.python.vision.gesture_recognizer import (
    GestureRecognizer,
    GestureRecognizerOptions,
)


def create_mediapipe_gesture_recognizer(
    model_path,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
):
    base_options = mp.tasks.BaseOptions(
        model_asset_path=str(model_path),
    )

    options = GestureRecognizerOptions(
        base_options=base_options,
        num_hands=num_hands,
        min_hand_detection_confidence=(
            min_hand_detection_confidence
        ),
        min_hand_presence_confidence=(
            min_hand_presence_confidence
        ),
        min_tracking_confidence=(
            min_tracking_confidence
        ),
    )

    return GestureRecognizer.create_from_options(
        options
    )
