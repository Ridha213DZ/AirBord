from app.core.enums.interaction_mode import InteractionMode


def test_interaction_mode_defines_basic_interaction_states():
    assert InteractionMode.IDLE.value == "idle"
    assert InteractionMode.DRAWING.value == "drawing"
    assert InteractionMode.TOOL_SELECTION.value == "tool_selection"
    assert InteractionMode.COLOR_SELECTION.value == "color_selection"
    assert InteractionMode.SIZE_SELECTION.value == "size_selection"
