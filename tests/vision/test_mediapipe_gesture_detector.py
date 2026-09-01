import mediapipe as mp
import numpy as np

from app.vision.mediapipe_gesture_detector import (
    MediaPipeGestureDetector,
)
from app.vision.mediapipe_gesture_recognizer_factory import (
    create_mediapipe_gesture_recognizer,
)


class FakeRecognizer:

    def __init__(self):
        self.received_image = None

    def recognize(self, image):
        self.received_image = image
        return "result"


def test_mediapipe_gesture_detector_can_be_created_with_recognizer():
    recognizer = FakeRecognizer()

    detector = MediaPipeGestureDetector(
        recognizer=recognizer,
    )

    assert detector is not None


def test_mediapipe_gesture_detector_converts_numpy_frame_and_returns_result():
    recognizer = FakeRecognizer()

    detector = MediaPipeGestureDetector(
        recognizer=recognizer,
    )

    frame = np.zeros(
        (100, 200, 3),
        dtype=np.uint8,
    )

    result = detector.detect(frame)

    assert result == "result"

    assert isinstance(
        recognizer.received_image,
        mp.Image,
    )


def test_mediapipe_gesture_detector_converts_bgr_frame_to_rgb():
    recognizer = FakeRecognizer()

    detector = MediaPipeGestureDetector(
        recognizer=recognizer,
    )

    frame = np.array(
        [[[10, 20, 30]]],
        dtype=np.uint8,
    )

    detector.detect(frame)

    assert recognizer.received_image.numpy_view()[
        0, 0
    ].tolist() == [
        30,
        20,
        10,
    ]


def test_mediapipe_gesture_detector_passes_existing_mediapipe_image_unchanged():
    recognizer = FakeRecognizer()

    detector = MediaPipeGestureDetector(
        recognizer=recognizer,
    )

    frame = np.zeros(
        (10, 10, 3),
        dtype=np.uint8,
    )

    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame,
    )

    result = detector.detect(image)

    assert result == "result"
    assert recognizer.received_image is image


def test_mediapipe_gesture_detector_creates_recognizer_when_not_provided():
    class FakeRecognizer:
        pass

    def recognizer_factory():
        return FakeRecognizer()

    detector = MediaPipeGestureDetector(
        recognizer_factory=recognizer_factory,
    )

    assert isinstance(
        detector.recognizer,
        FakeRecognizer,
    )


def test_mediapipe_gesture_detector_does_not_call_factory_when_recognizer_is_provided():
    class FakeRecognizer:
        pass

    calls = []

    def recognizer_factory():
        calls.append(True)
        return FakeRecognizer()

    recognizer = FakeRecognizer()

    MediaPipeGestureDetector(
        recognizer=recognizer,
        recognizer_factory=recognizer_factory,
    )

    assert calls == []


def test_mediapipe_gesture_recognizer_factory_creates_mediapipe_recognizer(
    monkeypatch,
    tmp_path,
):
    from mediapipe.tasks.python.vision.gesture_recognizer import (
        GestureRecognizer,
    )

    captured = {}

    def fake_create_from_options(options):
        captured["options"] = options
        return "recognizer"

    monkeypatch.setattr(
        GestureRecognizer,
        "create_from_options",
        fake_create_from_options,
    )

    model_path = tmp_path / "gesture_recognizer.task"

    recognizer = create_mediapipe_gesture_recognizer(
        model_path=model_path,
    )

    assert recognizer == "recognizer"
    assert captured["options"] is not None


def test_mediapipe_gesture_recognizer_factory_uses_model_path(
    monkeypatch,
    tmp_path,
):
    from mediapipe.tasks.python import BaseOptions
    from mediapipe.tasks.python.vision.gesture_recognizer import (
        GestureRecognizer,
    )

    captured = {}

    def fake_create_from_options(options):
        captured["options"] = options
        return "recognizer"

    monkeypatch.setattr(
        GestureRecognizer,
        "create_from_options",
        fake_create_from_options,
    )

    model_path = tmp_path / "gesture_recognizer.task"

    create_mediapipe_gesture_recognizer(
        model_path=model_path,
    )

    assert (
        captured["options"].base_options.model_asset_path
        == str(model_path)
    )


def test_mediapipe_gesture_detector_uses_factory_result():
    class FakeRecognizer:

        def recognize(self, image):
            return "result"

    calls = []

    def recognizer_factory():
        calls.append(True)
        return FakeRecognizer()

    detector = MediaPipeGestureDetector(
        recognizer_factory=recognizer_factory,
    )

    frame = np.zeros(
        (10, 10, 3),
        dtype=np.uint8,
    )

    result = detector.detect(frame)

    assert calls == [True]
    assert result == "result"


def test_mediapipe_gesture_recognizer_factory_configures_num_hands(
    monkeypatch,
    tmp_path,
):
    from mediapipe.tasks.python.vision.gesture_recognizer import (
        GestureRecognizer,
    )

    captured = {}

    def fake_create_from_options(options):
        captured["options"] = options
        return "recognizer"

    monkeypatch.setattr(
        GestureRecognizer,
        "create_from_options",
        fake_create_from_options,
    )

    model_path = tmp_path / "gesture_recognizer.task"

    create_mediapipe_gesture_recognizer(
        model_path=model_path,
        num_hands=1,
    )

    assert captured["options"].num_hands == 1


def test_mediapipe_gesture_recognizer_factory_configures_hand_detection_confidence(
    monkeypatch,
    tmp_path,
):
    from mediapipe.tasks.python.vision.gesture_recognizer import (
        GestureRecognizer,
    )

    captured = {}

    def fake_create_from_options(options):
        captured["options"] = options
        return "recognizer"

    monkeypatch.setattr(
        GestureRecognizer,
        "create_from_options",
        fake_create_from_options,
    )

    model_path = tmp_path / "gesture_recognizer.task"

    create_mediapipe_gesture_recognizer(
        model_path=model_path,
        min_hand_detection_confidence=0.5,
    )

    assert (
        captured["options"].min_hand_detection_confidence
        == 0.5
    )


def test_mediapipe_gesture_recognizer_factory_configures_hand_presence_confidence(
    monkeypatch,
    tmp_path,
):
    from mediapipe.tasks.python.vision.gesture_recognizer import (
        GestureRecognizer,
    )

    captured = {}

    def fake_create_from_options(options):
        captured["options"] = options
        return "recognizer"

    monkeypatch.setattr(
        GestureRecognizer,
        "create_from_options",
        fake_create_from_options,
    )

    model_path = tmp_path / "gesture_recognizer.task"

    create_mediapipe_gesture_recognizer(
        model_path=model_path,
        min_hand_presence_confidence=0.5,
    )

    assert (
        captured["options"].min_hand_presence_confidence
        == 0.5
    )


def test_mediapipe_gesture_recognizer_factory_configures_tracking_confidence(
    monkeypatch,
    tmp_path,
):
    from mediapipe.tasks.python.vision.gesture_recognizer import (
        GestureRecognizer,
    )

    captured = {}

    def fake_create_from_options(options):
        captured["options"] = options
        return "recognizer"

    monkeypatch.setattr(
        GestureRecognizer,
        "create_from_options",
        fake_create_from_options,
    )

    model_path = tmp_path / "gesture_recognizer.task"

    create_mediapipe_gesture_recognizer(
        model_path=model_path,
        min_tracking_confidence=0.5,
    )

    assert (
        captured["options"].min_tracking_confidence
        == 0.5
    )
