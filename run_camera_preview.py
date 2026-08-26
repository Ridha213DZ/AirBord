import sys

import cv2
from PySide6.QtWidgets import QApplication

from app.ui.camera_frame_source import CameraFrameSource
from app.ui.camera_preview_window import CameraPreviewWindow
from app.vision.backends.yunet_backend import YuNetBackend
from app.vision.face_detector import FaceDetector


MODEL_PATH = "models/face_detection_yunet_2026may.onnx"

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


def create_face_detector():
    yunet_detector = cv2.FaceDetectorYN.create(
        MODEL_PATH,
        "",
        (CAMERA_WIDTH, CAMERA_HEIGHT),
        0.6,
        0.3,
        5000,
    )

    backend = YuNetBackend(
        detector=yunet_detector,
    )

    return FaceDetector(
        backend=backend,
    )


def main():
    app = QApplication(sys.argv)

    source = CameraFrameSource.open(
        device=0,
    )

    face_detector = create_face_detector()

    window = CameraPreviewWindow(
        source=source,
        face_detector=face_detector,
    )

    window.setWindowTitle("AirBord - Camera Preview + YuNet")
    window.resize(800, 600)
    window.show()

    exit_code = app.exec()

    source.close()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
