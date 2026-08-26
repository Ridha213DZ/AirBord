import numpy as np

from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen
from PySide6.QtWidgets import QWidget

from app.vision.models.detected_face import DetectedFace


class CameraPreview(QWidget):

    def __init__(self):
        super().__init__()

        self.frame = None
        self.image = None
        self.faces: list[DetectedFace] = []
        self.recognition_results = []

        self.setMinimumSize(320, 240)

    def set_frame(self, frame: np.ndarray):
        self.frame = frame

        height, width, channels = frame.shape

        self.image = QImage(
            frame.data,
            width,
            height,
            width * channels,
            QImage.Format_BGR888,
        ).copy()

        self.update()

    def set_faces(self, faces: list[DetectedFace]):
        self.faces = list(faces)
        self.update()

    def set_recognition_results(self, results):
        self.recognition_results = list(results)
        self.update()

    def update_from_source(self, source):
        frame = source.read()

        if frame is not None:
            self.set_frame(frame)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.image is None:
            return

        painter = QPainter(self)

        painter.drawImage(
            self.rect(),
            self.image,
        )

        if self.image.width() == 0 or self.image.height() == 0:
            painter.end()
            return

        scale_x = self.width() / self.image.width()
        scale_y = self.height() / self.image.height()

        pen = QPen(QColor(0, 255, 0))
        pen.setWidth(2)

        painter.setPen(pen)

        font = QFont()
        font.setPointSize(10)

        painter.setFont(font)

        if self.recognition_results:
            self._draw_recognition_results(
                painter,
                scale_x,
                scale_y,
            )
        else:
            self._draw_faces(
                painter,
                scale_x,
                scale_y,
            )

        painter.end()

    def _draw_faces(
        self,
        painter,
        scale_x,
        scale_y,
    ):
        for face in self.faces:
            painter.drawRect(
                int(face.x * scale_x),
                int(face.y * scale_y),
                int(face.width * scale_x),
                int(face.height * scale_y),
            )

    def _draw_recognition_results(
        self,
        painter,
        scale_x,
        scale_y,
    ):
        for result in self.recognition_results:
            face = result.face

            x = int(face.x * scale_x)
            y = int(face.y * scale_y)
            width = int(face.width * scale_x)
            height = int(face.height * scale_y)

            painter.drawRect(
                x,
                y,
                width,
                height,
            )

            label = "Unknown"

            if result.identity is not None:
                label = f"ID: {str(result.identity.id)[:8]}"

            painter.drawText(
                x,
                max(15, y - 5),
                label,
            )
