from PySide6.QtWidgets import QApplication, QWidget

from app.ui.camera_preview_window import CameraPreviewWindow


class FakeCameraFrameSource:

    def __init__(self):
        self.closed = False

    def read(self):
        return None

    def close(self):
        self.closed = True


def test_camera_preview_window_is_qt_widget():
    app = QApplication.instance() or QApplication([])

    window = CameraPreviewWindow(
        source=FakeCameraFrameSource(),
    )

    assert isinstance(window, QWidget)


def test_camera_preview_window_contains_camera_preview():
    app = QApplication.instance() or QApplication([])

    window = CameraPreviewWindow(
        source=FakeCameraFrameSource(),
    )

    assert window.preview is not None


def test_camera_preview_window_updates_preview_from_source():
    import numpy as np

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    class FakeCameraFrameSource:
        def __init__(self):
            self.read_count = 0

        def read(self):
            self.read_count += 1
            return frame

        def close(self):
            pass

    app = QApplication.instance() or QApplication([])

    source = FakeCameraFrameSource()

    window = CameraPreviewWindow(
        source=source,
    )

    window.update_frame()

    assert source.read_count == 1
    assert window.preview.image is not None


def test_camera_preview_window_has_update_timer():
    app = QApplication.instance() or QApplication([])

    class FakeCameraFrameSource:
        def read(self):
            return None

        def close(self):
            pass

    source = FakeCameraFrameSource()

    window = CameraPreviewWindow(
        source=source,
    )

    assert window.timer is not None
