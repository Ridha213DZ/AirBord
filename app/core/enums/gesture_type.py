from enum import Enum


class GestureType(str, Enum):
    NONE = "none"

    DRAW_START = "draw_start"
    DRAW_MOVE = "draw_move"
    DRAW_END = "draw_end"

    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"

    SELECT = "select"
    ERASE = "erase"