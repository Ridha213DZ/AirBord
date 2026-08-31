from app.core.enums.hand_gesture import HandGesture
from app.core.enums.interaction_action import InteractionAction
from app.core.enums.interaction_zone import InteractionZone


def test_open_gesture_in_undo_zone_produces_undo_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.OPEN,
        zone=InteractionZone.UNDO,
    )

    assert action == InteractionAction.UNDO


def test_open_gesture_in_redo_zone_produces_redo_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.OPEN,
        zone=InteractionZone.REDO,
    )

    assert action == InteractionAction.REDO


def test_fist_gesture_in_canvas_zone_produces_draw_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.FIST,
        zone=InteractionZone.CANVAS,
    )

    assert action == InteractionAction.DRAW


def test_fist_gesture_outside_canvas_produces_no_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.FIST,
        zone=InteractionZone.COLOR_RING,
    )

    assert action is None


def test_open_gesture_in_color_ring_produces_select_color_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.OPEN,
        zone=InteractionZone.COLOR_RING,
    )

    assert action == InteractionAction.SELECT_COLOR


def test_open_gesture_in_eraser_ring_produces_toggle_eraser_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.OPEN,
        zone=InteractionZone.ERASER_RING,
    )

    assert action == InteractionAction.TOGGLE_ERASER


def test_open_gesture_in_tool_ring_produces_select_tool_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.OPEN,
        zone=InteractionZone.TOOL_RING,
    )

    assert action == InteractionAction.SELECT_TOOL


def test_open_gesture_in_canvas_produces_no_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.OPEN,
        zone=InteractionZone.CANVAS,
    )

    assert action is None


def test_open_gesture_in_unknown_zone_produces_no_action():
    from app.application.services.interaction_action_resolver import (
        InteractionActionResolver,
    )

    resolver = InteractionActionResolver()

    action = resolver.resolve(
        gesture=HandGesture.OPEN,
        zone=InteractionZone.UNKNOWN,
    )

    assert action is None
