import numpy as np
from PySide6.QtWidgets import QApplication

from app.ui.camera_preview import CameraPreview
from app.vision.models.detected_face import DetectedFace


def test_camera_preview_accepts_detected_faces():
    app = QApplication.instance() or QApplication([])

    preview = CameraPreview()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    face = DetectedFace(
        x=100,
        y=80,
        width=200,
        height=200,
        confidence=0.95,
    )

    preview.set_frame(frame)
    preview.set_faces([face])

    assert preview.faces == [face]


def test_camera_preview_updates_when_faces_are_set(monkeypatch):
    app = QApplication.instance() or QApplication([])

    preview = CameraPreview()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    face = DetectedFace(
        x=100,
        y=80,
        width=200,
        height=200,
        confidence=0.95,
    )

    updated = {"called": False}

    def fake_update():
        updated["called"] = True

    monkeypatch.setattr(
        preview,
        "update",
        fake_update,
    )

    preview.set_frame(frame)
    preview.set_faces([face])

    assert preview.faces == [face]
    assert updated["called"]


def test_camera_preview_draws_face_rectangle():
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

    preview.set_frame(frame)
    preview.set_faces([face])

    preview.resize(320, 240)

    image = preview.grab().toImage()

    assert image.pixelColor(64, 48) != image.pixelColor(160, 120)
