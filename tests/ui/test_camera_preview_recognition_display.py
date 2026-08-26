import numpy as np

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication

from app.ui.camera_preview import CameraPreview
from app.vision.face_recognition import FaceRecognitionResult
from app.vision.models.detected_face import DetectedFace


def test_camera_preview_draws_unknown_face_rectangle():
    app = QApplication.instance() or QApplication([])

    preview = CameraPreview()

    frame = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    face = DetectedFace(
        x=20,
        y=20,
        width=40,
        height=40,
        confidence=0.95,
    )

    result = FaceRecognitionResult(
        face=face,
        identity=None,
    )

    preview.set_frame(frame)
    preview.set_recognition_results([result])

    preview.resize(320, 240)

    app.processEvents()
    preview.repaint()
    app.processEvents()

    image = preview.grab().toImage()

    border_color = image.pixelColor(64, 48)
    background_color = image.pixelColor(160, 120)

    assert border_color != background_color
    assert border_color != QColor(0, 0, 0)
