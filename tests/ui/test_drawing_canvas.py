from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QImage, QMouseEvent, QPainter
from PySide6.QtWidgets import QApplication, QWidget

from app.core.models.page import Page
from app.core.models.point import Point
from app.core.models.stroke import Stroke
from app.ui.drawing_canvas import DrawingCanvas


def test_drawing_canvas_is_qt_widget():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    assert isinstance(canvas, QWidget)


def test_drawing_canvas_accepts_page():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()
    page = Page()

    canvas.set_page(page)

    assert canvas.page is page


def test_drawing_canvas_accepts_page_with_stroke():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    page = Page()

    stroke = Stroke(
        color="#FF0000",
        width=8.0,
    )

    stroke.add_point(
        Point(
            x=10.0,
            y=20.0,
        )
    )

    stroke.add_point(
        Point(
            x=100.0,
            y=120.0,
        )
    )

    page.add_stroke(stroke)

    canvas.set_page(page)

    assert canvas.page is page
    assert canvas.page.stroke_count == 1


def test_drawing_canvas_paints_page_strokes():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    page = Page()

    stroke = Stroke(
        color="#FF0000",
        width=8.0,
    )

    stroke.add_point(
        Point(
            x=20.0,
            y=20.0,
        )
    )

    stroke.add_point(
        Point(
            x=100.0,
            y=100.0,
        )
    )

    page.add_stroke(stroke)
    canvas.set_page(page)

    canvas.resize(200, 200)

    image = QImage(
        200,
        200,
        QImage.Format_RGB32,
    )
    image.fill(0)

    painter = QPainter(image)

    try:
        canvas.render(
            painter,
            canvas.rect().topLeft(),
        )
    finally:
        painter.end()

    assert image.pixelColor(20, 20) != image.pixelColor(0, 0)


def test_drawing_canvas_paints_single_point_stroke():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    page = Page()

    stroke = Stroke(
        color="#FF0000",
        width=8.0,
    )

    stroke.add_point(
        Point(
            x=50.0,
            y=50.0,
        )
    )

    page.add_stroke(stroke)
    canvas.set_page(page)

    canvas.resize(100, 100)

    image = QImage(
        100,
        100,
        QImage.Format_RGB32,
    )
    image.fill(0)

    painter = QPainter(image)

    try:
        canvas.render(
            painter,
            canvas.rect().topLeft(),
        )
    finally:
        painter.end()

    assert image.pixelColor(50, 50) != image.pixelColor(0, 0)


def test_drawing_canvas_starts_stroke_on_mouse_press():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPoint(40, 50),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mousePressEvent(event)

    assert canvas.current_stroke is not None
    assert len(canvas.current_stroke.points) == 1
    assert canvas.current_stroke.points[0] == Point(
        x=40.0,
        y=50.0,
    )


def test_drawing_canvas_adds_point_on_mouse_move():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    press_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPoint(40, 50),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mousePressEvent(press_event)

    move_event = QMouseEvent(
        QMouseEvent.Type.MouseMove,
        QPoint(60, 70),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mouseMoveEvent(move_event)

    assert canvas.current_stroke is not None
    assert len(canvas.current_stroke.points) == 2
    assert canvas.current_stroke.points[1] == Point(
        x=60.0,
        y=70.0,
    )


def test_drawing_canvas_uses_drawing_service_to_add_completed_stroke():
    app = QApplication.instance() or QApplication([])

    class FakeDrawingService:

        def __init__(self):
            self.added_strokes = []

        def add_stroke(self, stroke):
            self.added_strokes.append(stroke)

    service = FakeDrawingService()

    canvas = DrawingCanvas(
        drawing_service=service,
    )

    press_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPoint(40, 50),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mousePressEvent(press_event)

    move_event = QMouseEvent(
        QMouseEvent.Type.MouseMove,
        QPoint(60, 70),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mouseMoveEvent(move_event)

    release_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        QPoint(80, 90),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mouseReleaseEvent(release_event)

    assert len(service.added_strokes) == 1

    stroke = service.added_strokes[0]

    assert len(stroke.points) == 3
    assert stroke.points[0] == Point(
        x=40.0,
        y=50.0,
    )
    assert stroke.points[1] == Point(
        x=60.0,
        y=70.0,
    )
    assert stroke.points[2] == Point(
        x=80.0,
        y=90.0,
    )


def test_drawing_canvas_ignores_mouse_release_without_active_stroke():
    app = QApplication.instance() or QApplication([])

    class FakeDrawingService:

        def __init__(self):
            self.added_strokes = []

        def add_stroke(self, stroke):
            self.added_strokes.append(stroke)

    service = FakeDrawingService()

    canvas = DrawingCanvas(
        drawing_service=service,
    )

    release_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        QPoint(80, 90),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mouseReleaseEvent(release_event)

    assert canvas.current_stroke is None
    assert service.added_strokes == []


def test_drawing_canvas_does_not_modify_page_directly_without_drawing_service():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    page = Page()
    canvas.set_page(page)

    press_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPoint(40, 50),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mousePressEvent(press_event)

    release_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        QPoint(80, 90),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mouseReleaseEvent(release_event)

    assert page.stroke_count == 0


def test_drawing_canvas_does_not_add_empty_stroke():
    app = QApplication.instance() or QApplication([])

    class FakeDrawingService:

        def __init__(self):
            self.added_strokes = []

        def add_stroke(self, stroke):
            self.added_strokes.append(stroke)

    service = FakeDrawingService()

    canvas = DrawingCanvas(
        drawing_service=service,
    )

    canvas.current_stroke = Stroke()

    release_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        QPoint(80, 90),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    canvas.mouseReleaseEvent(release_event)

    assert canvas.current_stroke is None
    assert service.added_strokes == []


def test_drawing_canvas_accepts_cursor_position():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()

    position = Point(
        x=150.0,
        y=200.0,
    )

    canvas.set_cursor_position(position)

    assert canvas.cursor_position == position


# التحقق من أن لوحة الرسم تقوم برسم مؤشر اليد بصرياً عند تحديد موضعه
def test_drawing_canvas_paints_cursor():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()
    canvas.resize(100, 100)

    canvas.set_cursor_position(
        Point(
            x=50.0,
            y=50.0,
        )
    )

    image = QImage(
        100,
        100,
        QImage.Format_RGB32,
    )
    image.fill(0)

    painter = QPainter(image)

    try:
        canvas.render(
            painter,
            canvas.rect().topLeft(),
        )
    finally:
        painter.end()

    assert image.pixelColor(50, 50) != image.pixelColor(0, 0)


# التحقق من أن لوحة الرسم تعرض السكتة الجارية (current_stroke) آنياً أثناء الرسم
def test_drawing_canvas_paints_current_stroke():
    app = QApplication.instance() or QApplication([])

    canvas = DrawingCanvas()
    canvas.resize(100, 100)

    stroke = Stroke(
        color="#FF0000",
        width=8.0,
    )
    stroke.add_point(
        Point(
            x=30.0,
            y=30.0,
        )
    )

    canvas.set_current_stroke(stroke)

    assert canvas.current_stroke is stroke

    image = QImage(
        100,
        100,
        QImage.Format_RGB32,
    )
    image.fill(0)

    painter = QPainter(image)

    try:
        canvas.render(
            painter,
            canvas.rect().topLeft(),
        )
    finally:
        painter.end()

    assert image.pixelColor(30, 30) != image.pixelColor(0, 0)
