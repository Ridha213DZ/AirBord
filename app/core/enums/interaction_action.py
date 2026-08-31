from enum import Enum


class InteractionAction(str, Enum):
    UNDO = "undo"
    REDO = "redo"
    DRAW = "draw"
    SELECT_COLOR = "select_color"
    TOGGLE_ERASER = "toggle_eraser"
    SELECT_TOOL = "select_tool"