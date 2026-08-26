import cv2
import pytest

from app.ui.camera_frame_source import CameraFrameSource


@pytest.mark.integration
def test_camera_frame_source_reads_real_camera_frame():
    source = CameraFrameSource.open(
        device=0,
    )

    try:
        assert source.capture.isOpened()

        frame = source.read()

        assert frame is not None
        assert frame.shape == (480, 640, 3)
        assert frame.dtype.name == "uint8"

    finally:
        source.close()
