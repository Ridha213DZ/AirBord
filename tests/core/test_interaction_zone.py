from app.core.enums.interaction_zone import InteractionZone


def test_interaction_zone_defines_canvas():
    assert InteractionZone.CANVAS.value == "canvas"


def test_interaction_zone_defines_color_ring():
    assert InteractionZone.COLOR_RING.value == "color_ring"


def test_interaction_zone_defines_eraser_ring():
    assert InteractionZone.ERASER_RING.value == "eraser_ring"


def test_interaction_zone_defines_tool_ring():
    assert InteractionZone.TOOL_RING.value == "tool_ring"


def test_interaction_zone_defines_undo():
    assert InteractionZone.UNDO.value == "undo"


def test_interaction_zone_defines_redo():
    assert InteractionZone.REDO.value == "redo"


def test_interaction_zone_defines_unknown():
    assert InteractionZone.UNKNOWN.value == "unknown"
