from app.core.enums.interaction_action import InteractionAction
from app.core.enums.interaction_mode import InteractionMode
from app.core.models.point import Point
from app.core.models.stroke import Stroke


class InteractionActionHandler:

    def __init__(self, history_manager=None):
        self.is_drawing = False
        self.eraser_enabled = False
        self.mode = InteractionMode.IDLE
        self.history_manager = history_manager
        self.current_stroke: Stroke | None = None

    def handle(
        self,
        action: InteractionAction,
    ) -> None:

        if action == InteractionAction.DRAW:
            self.is_drawing = True
            self.mode = InteractionMode.DRAWING

            if self.current_stroke is None:
                self.current_stroke = Stroke()

        elif action == InteractionAction.TOGGLE_ERASER:
            self.eraser_enabled = not self.eraser_enabled

        elif action == InteractionAction.SELECT_COLOR:
            self.mode = InteractionMode.COLOR_SELECTION

        elif action == InteractionAction.SELECT_TOOL:
            self.mode = InteractionMode.TOOL_SELECTION

        elif action == InteractionAction.UNDO:
            if self.history_manager is not None:
                self.history_manager.undo()

        elif action == InteractionAction.REDO:
            if self.history_manager is not None:
                self.history_manager.redo()


    def add_point(
        self,
        point: Point,
    ) -> None:
        if (
            not self.is_drawing
            or self.current_stroke is None
        ):
            return

        self.current_stroke.add_point(
            point
        )


    def finish_stroke(
        self,
    ) -> Stroke | None:
        if self.current_stroke is None:
            self.is_drawing = False
            return None

        if not self.current_stroke.points:
            self.current_stroke = None
            self.is_drawing = False
            return None

        completed_stroke = self.current_stroke

        self.current_stroke = None
        self.is_drawing = False

        return completed_stroke
