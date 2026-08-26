from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout

from app.ui.camera_preview import CameraPreview


class CameraPreviewWindow(QWidget):

    def __init__(
        self,
        source,
        face_detector=None,
        face_recognition=None,
        identities=None,
    ):
        super().__init__()

        self.source = source
        self.face_detector = face_detector
        self.face_recognition = face_recognition
        self.identities = identities or []

        self.preview = CameraPreview()

        layout = QVBoxLayout(self)
        layout.addWidget(self.preview)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    def update_frame(self):
        frame = self.source.read()

        if frame is None:
            return

        faces = []

        if self.face_detector is not None:
            faces = self.face_detector.detect(frame)

        if self.face_recognition is not None:
            results = self.face_recognition.recognize(
                frame=frame,
                faces=faces,
                identities=self.identities,
            )

            self.preview.set_recognition_results(results)

        self.preview.set_frame(frame)
        self.preview.set_faces(faces)
