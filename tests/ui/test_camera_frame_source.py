import numpy as np

from app.ui.camera_frame_source import CameraFrameSource


class FakeCapture:

    def __init__(self):
        self.opened = True
        self.released = False

    def isOpened(self):
        return self.opened

    def read(self):
        return (
            True,
            np.zeros(
                (480, 640, 3),
                dtype=np.uint8,
            ),
        )

    def release(self):
        self.released = True


def test_camera_frame_source_reads_frame():
    capture = FakeCapture()

    source = CameraFrameSource(
        capture=capture,
    )

    frame = source.read()

    assert isinstance(frame, np.ndarray)
    assert frame.shape == (480, 640, 3)


def test_camera_frame_source_releases_capture():
    capture = FakeCapture()

    source = CameraFrameSource(
        capture=capture,
    )

    source.close()

    assert capture.released is True


def test_camera_frame_source_can_open_opencv_camera(monkeypatch):
    import cv2

    created = {}

    class FakeVideoCapture:
        def __init__(self, device, backend):
            created["device"] = device
            created["backend"] = backend

    monkeypatch.setattr(
        cv2,
        "VideoCapture",
        FakeVideoCapture,
    )

    source = CameraFrameSource.open(
        device=0,
    )

    assert created["device"] == 0
    assert created["backend"] == cv2.CAP_V4L2
    assert isinstance(source.capture, FakeVideoCapture)
