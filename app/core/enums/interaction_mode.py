from enum import Enum


class InteractionMode(str, Enum):
    IDLE = "idle"
    DRAWING = "drawing"
    TOOL_SELECTION = "tool_selection"
    COLOR_SELECTION = "color_selection"
    SIZE_SELECTION = "size_selection"
