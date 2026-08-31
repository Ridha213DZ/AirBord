from app.core.enums.interaction_zone import InteractionZone
from app.core.models.point import Point


class InteractionZoneDetector:

    def __init__(
        self,
        screen_width: int = 1920,
        screen_height: int = 1080,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def detect(
        self,
        position: Point,
    ) -> InteractionZone:

        if position.x <= self.screen_width * 0.15:
            return InteractionZone.COLOR_RING

        if position.x >= self.screen_width * 0.85:
            return InteractionZone.ERASER_RING

        if position.y >= self.screen_height * 0.85:
            if position.x < self.screen_width * 0.5:
                return InteractionZone.UNDO

            return InteractionZone.REDO
        if position.y <= self.screen_height * 0.15:
            return InteractionZone.TOOL_RING

        return InteractionZone.CANVAS
