import numpy as np
from PySide6.QtWidgets import QApplication, QWidget

from app.ui.camera_preview import CameraPreview


def test_camera_preview_is_qt_widget():
    app = QApplication.instance() or QApplication([])

    preview = CameraPreview()

    assert isinstance(preview, QWidget)


def test_camera_preview_accepts_frame():
    app = QApplication.instance() or QApplication([])

    preview = CameraPreview()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    preview.set_frame(frame)

    assert preview.frame is frame


def test_camera_preview_converts_frame_to_display_image():
    app = QApplication.instance() or QApplication([])

    preview = CameraPreview()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    preview.set_frame(frame)

    assert preview.image is not None
    assert preview.image.width() == 640
    assert preview.image.height() == 480


import numpy as np

from app.ui.camera_preview import CameraPreview


class FakeCameraFrameSource:

    def __init__(self, frame):
        self.frame = frame

    def read(self):
        return self.frame


def test_camera_preview_can_receive_frame_from_camera_source():
    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    source = FakeCameraFrameSource(
        frame=frame,
    )

    preview = CameraPreview()

    preview.update_from_source(
        source,
    )

    assert preview.image is not None


def test_camera_preview_can_paint_frame():
    app = QApplication.instance() or QApplication([])

    preview = CameraPreview()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    preview.set_frame(frame)

    assert preview.image is not None
    assert preview.image.size().width() == 640
    assert preview.image.size().height() == 480
