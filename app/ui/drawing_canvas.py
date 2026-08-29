from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QWidget

from app.application.services.drawing_service import DrawingService
from app.core.models.page import Page
from app.core.models.point import Point
from app.core.models.stroke import Stroke


class DrawingCanvas(QWidget):

    def __init__(
        self,
        drawing_service: DrawingService | None = None,
    ):
        super().__init__()

        self.page: Page | None = None
        self.current_stroke: Stroke | None = None
        self.drawing_service = drawing_service

    def set_page(self, page: Page) -> None:
        self.page = page
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        if self.page is None:
            return

        painter = QPainter(self)

        for stroke in self.page.strokes:
            if not stroke.points:
                continue

            pen = QPen()
            pen.setColor(stroke.color)
            pen.setWidthF(stroke.width)

            painter.setPen(pen)

            if len(stroke.points) == 1:
                point = stroke.points[0]

                painter.drawPoint(
                    point.x,
                    point.y,
                )

                continue

            for first, second in zip(
                stroke.points,
                stroke.points[1:],
            ):
                painter.drawLine(
                    first.x,
                    first.y,
                    second.x,
                    second.y,
                )

        painter.end()

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return

        self.current_stroke = Stroke()

        self.current_stroke.add_point(
            Point(
                x=event.position().x(),
                y=event.position().y(),
            )
        )

        self.update()

    def mouseMoveEvent(self, event) -> None:
        if self.current_stroke is None:
            return

        if not event.buttons() & Qt.MouseButton.LeftButton:
            return

        self.current_stroke.add_point(
            Point(
                x=event.position().x(),
                y=event.position().y(),
            )
        )

        self.update()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return

        if self.current_stroke is None:
            return

        stroke = self.current_stroke

        if not stroke.points:
            self.current_stroke = None
            return

        stroke.add_point(
            Point(
                x=event.position().x(),
                y=event.position().y(),
            )
        )

        self.current_stroke = None

        if self.drawing_service is not None:
            self.drawing_service.add_stroke(stroke)

        self.update()
