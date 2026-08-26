import numpy as np

from app.vision.backends.yunet_backend import YuNetBackend


class FakeYuNetDetector:

    def detect(self, frame):
        return (
            None,
            np.array(
                [
                    [
                        100.0,
                        80.0,
                        200.0,
                        200.0,
                        140.0,
                        160.0,
                        0.95,
                    ]
                ],
                dtype=np.float32,
            ),
        )


def test_yunet_backend_returns_raw_detections():
    backend = YuNetBackend(
        detector=FakeYuNetDetector(),
    )

    frame = object()

    detections = backend.detect(frame)

    assert len(detections) == 1

    import pytest

    # ...

    assert detections[0][:6] == [
        100.0,
        80.0,
        200.0,
        200.0,
        140.0,
        160.0,
    ]

    assert detections[0][6] == pytest.approx(0.95)


def test_yunet_backend_returns_empty_list_when_no_face_is_detected():
    class EmptyYuNetDetector:

        def detect(self, frame):
            return (
                None,
                None,
            )

    backend = YuNetBackend(
        detector=EmptyYuNetDetector(),
    )

    frame = object()

    detections = backend.detect(frame)

    assert detections == []
