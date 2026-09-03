from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

from app.application.canvas_coordinate_mapper import (
    CanvasCoordinateMapper,
)
from app.core.models.page import Page
from app.core.models.point import Point
from app.ui.drawing_canvas import DrawingCanvas


def test_canvas_receives_mapped_hand_position_as_local_coordinate():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    page = Page()
    canvas.set_page(page)

    mapper = CanvasCoordinateMapper(
        screen_width=1920,
        screen_height=1080,
        margin_ratio=0.15,
    )

    screen_position = Point(
        x=960.0,
        y=540.0,
    )

    canvas_position = mapper.map(
        screen_position
    )

    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPoint(
            int(canvas_position.x),
            int(canvas_position.y),
        ),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mousePressEvent(event)

    assert canvas.current_stroke is not None

    assert canvas.current_stroke.points == [
        Point(
            x=672.0,
            y=378.0,
        ),
    ]

    app.processEvents()
