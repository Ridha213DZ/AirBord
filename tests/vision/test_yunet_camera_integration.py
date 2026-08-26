import cv2
import pytest

from app.ui.camera_frame_source import CameraFrameSource
from app.vision.backends.yunet_backend import YuNetBackend
from app.vision.face_detector import FaceDetector


MODEL_PATH = "models/face_detection_yunet_2026may.onnx"


@pytest.mark.integration
def test_real_camera_yunet_pipeline_can_detect_faces():
    source = CameraFrameSource.open(
        device=0,
    )

    detector = cv2.FaceDetectorYN.create(
        MODEL_PATH,
        "",
        (640, 480),
        0.6,
        0.3,
        5000,
    )

    backend = YuNetBackend(
        detector=detector,
    )

    face_detector = FaceDetector(
        backend=backend,
    )

    try:
        frame = None

        for _ in range(30):
            frame = source.read()

            if frame is not None:
                break

        assert frame is not None

        height, width = frame.shape[:2]

        detector.setInputSize(
            (width, height),
        )

        faces = face_detector.detect(frame)

        assert isinstance(faces, list)

    finally:
        source.close()
