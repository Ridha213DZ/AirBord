from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout

from app.core.enums.application_mode import ApplicationMode
from app.ui.camera_preview import CameraPreview


class CameraPreviewWindow(QWidget):

    def __init__(
        self,
        source,
        face_detector=None,
        face_recognition=None,
        identities=None,
        face_profile_service=None,
        application_state=None,
        hand_gesture_pipeline=None,
    ):
        super().__init__()

        self.source = source
        self.face_detector = face_detector
        self.face_recognition = face_recognition
        self.identities = identities or []
        self.face_profile_service = face_profile_service

        self.application_state = application_state
        self.hand_gesture_pipeline = (
            hand_gesture_pipeline
        )

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

        if (
            self.application_state is not None
            and self.application_state.mode
            == ApplicationMode.DRAWING
        ):
            if self.hand_gesture_pipeline is not None:
                self.hand_gesture_pipeline.process(
                    frame
                )

            self.preview.set_frame(frame)

            return

        faces = []

        if self.face_detector is not None:
            faces = self.face_detector.detect(frame)

        if self.face_profile_service is not None:
            results = self.face_profile_service.process(
                frame=frame,
                faces=faces,
            )

            self.preview.set_recognition_results(results)

        elif self.face_recognition is not None:
            results = self.face_recognition.recognize(
                frame=frame,
                faces=faces,
                identities=self.identities,
            )

            self.preview.set_recognition_results(results)

        self.preview.set_frame(frame)
        self.preview.set_faces(faces)
