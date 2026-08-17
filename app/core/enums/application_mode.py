from enum import Enum


class ApplicationMode(str, Enum):
    IDLE = "idle"
    PROFILE_CREATION = "profile_creation"
    PROFILE_ACTIVE = "profile_active"
    DRAWING = "drawing"