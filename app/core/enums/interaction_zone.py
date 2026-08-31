from enum import Enum


class InteractionZone(str, Enum):
    UNKNOWN = "unknown"

    CANVAS = "canvas"

    COLOR_RING = "color_ring"

    ERASER_RING = "eraser_ring"

    TOOL_RING = "tool_ring"

    UNDO = "undo"

    REDO = "redo"
