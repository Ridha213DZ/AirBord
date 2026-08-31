from app.application.services.interaction_action_handler import (
    InteractionActionHandler,
)
from app.core.enums.interaction_action import InteractionAction
from app.core.enums.interaction_mode import InteractionMode
from app.core.models.point import Point

def test_interaction_action_handler_starts_drawing_on_draw_action():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.DRAW
    )

    assert handler.is_drawing is True


def test_interaction_action_handler_enables_eraser_on_toggle_eraser_action():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.TOGGLE_ERASER
    )

    assert handler.eraser_enabled is True


def test_interaction_action_handler_toggles_eraser_off():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.TOGGLE_ERASER
    )

    handler.handle(
        InteractionAction.TOGGLE_ERASER
    )

    assert handler.eraser_enabled is False


def test_interaction_action_handler_enters_color_selection_on_select_color():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.SELECT_COLOR
    )

    assert handler.mode == InteractionMode.COLOR_SELECTION


def test_interaction_action_handler_enters_tool_selection_on_select_tool():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.SELECT_TOOL
    )

    assert handler.mode == InteractionMode.TOOL_SELECTION


def test_interaction_action_handler_requests_undo():
    class FakeHistoryManager:

        def __init__(self):
            self.undo_called = False

        def undo(self):
            self.undo_called = True

    history_manager = FakeHistoryManager()

    handler = InteractionActionHandler(
        history_manager=history_manager,
    )

    handler.handle(
        InteractionAction.UNDO
    )

    assert history_manager.undo_called is True


def test_interaction_action_handler_requests_redo():
    class FakeHistoryManager:

        def __init__(self):
            self.redo_called = False

        def redo(self):
            self.redo_called = True

    history_manager = FakeHistoryManager()

    handler = InteractionActionHandler(
        history_manager=history_manager,
    )

    handler.handle(
        InteractionAction.REDO
    )

    assert history_manager.redo_called is True


def test_interaction_action_handler_starts_current_stroke_on_draw():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.DRAW
    )

    assert handler.current_stroke is not None
    assert handler.current_stroke.is_empty()


def test_interaction_action_handler_adds_point_to_current_stroke():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.DRAW
    )

    point = Point(500, 400)

    handler.add_point(point)

    assert handler.current_stroke.points == [
        point,
    ]


def test_interaction_action_handler_does_not_start_new_stroke_when_already_drawing():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.DRAW
    )

    first_stroke = handler.current_stroke

    handler.handle(
        InteractionAction.DRAW
    )

    assert handler.current_stroke is first_stroke


def test_interaction_action_handler_finishes_current_stroke():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.DRAW
    )

    point = Point(500, 400)

    handler.add_point(point)

    completed_stroke = handler.finish_stroke()

    assert completed_stroke is not None
    assert completed_stroke.points == [point]
    assert handler.is_drawing is False
    assert handler.current_stroke is None


def test_interaction_action_handler_finish_stroke_returns_none_without_current_stroke():
    handler = InteractionActionHandler()

    completed_stroke = handler.finish_stroke()

    assert completed_stroke is None
    assert handler.is_drawing is False
    assert handler.current_stroke is None


def test_interaction_action_handler_does_not_finish_empty_stroke():
    handler = InteractionActionHandler()

    handler.handle(
        InteractionAction.DRAW
    )

    completed_stroke = handler.finish_stroke()

    assert completed_stroke is None
    assert handler.is_drawing is False
    assert handler.current_stroke is None
