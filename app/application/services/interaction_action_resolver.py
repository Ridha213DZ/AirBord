from app.core.enums.hand_gesture import HandGesture
from app.core.enums.interaction_action import InteractionAction
from app.core.enums.interaction_zone import InteractionZone


class InteractionActionResolver:

    def resolve(
        self,
        gesture: HandGesture,
        zone: InteractionZone,
    ) -> InteractionAction | None:

        if (
            gesture == HandGesture.OPEN
            and zone == InteractionZone.UNDO
        ):
            return InteractionAction.UNDO

        if (
            gesture == HandGesture.OPEN
            and zone == InteractionZone.REDO
        ):
            return InteractionAction.REDO

        if (
            gesture == HandGesture.FIST
            and zone == InteractionZone.CANVAS
        ):
            return InteractionAction.DRAW
        if (
            gesture == HandGesture.OPEN
            and zone == InteractionZone.COLOR_RING
        ):
            return InteractionAction.SELECT_COLOR
        if (
            gesture == HandGesture.OPEN
            and zone == InteractionZone.ERASER_RING
        ):
            return InteractionAction.TOGGLE_ERASER
        if (
            gesture == HandGesture.OPEN
            and zone == InteractionZone.TOOL_RING
        ):
            return InteractionAction.SELECT_TOOL

        return None
