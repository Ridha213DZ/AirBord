from app.application.services.interaction_action_resolver import (
    InteractionActionResolver,
)
from app.application.services.interaction_zone_detector import (
    InteractionZoneDetector,
)
from app.core.enums.hand_gesture import HandGesture
from app.core.enums.interaction_mode import InteractionMode
from app.core.enums.interaction_zone import InteractionZone
from app.core.models.hand_gesture_event import HandGestureEvent


class HandGestureController:

    def __init__(
        self,
        screen_width: int = 1920,
        screen_height: int = 1080,
        zone_detector=None,
        action_resolver=None,
        action_handler=None,
        drawing_service=None,
    ):
        self.is_drawing = False
        self.mode = InteractionMode.IDLE

        self.zone_detector = zone_detector or InteractionZoneDetector(
            screen_width=screen_width,
            screen_height=screen_height,
        )

        self.action_resolver = action_resolver or InteractionActionResolver()
        self.action_handler = action_handler
        self.drawing_service = drawing_service

        self.zone = InteractionZone.UNKNOWN

    def handle(
        self,
        event: HandGestureEvent,
    ) -> None:

        if event.position is not None:
            self.zone = self.zone_detector.detect(
                event.position
            )

        action = self.action_resolver.resolve(
            gesture=event.gesture,
            zone=self.zone,
        )

        if (
            action is not None
            and self.action_handler is not None
        ):
            self.action_handler.handle(action)

        if event.gesture == HandGesture.FIST:
            self.is_drawing = True
            self.mode = InteractionMode.DRAWING

            if (
                event.position is not None
                and self.action_handler is not None
            ):
                self.action_handler.add_point(
                    event.position
                )

        elif event.gesture == HandGesture.OPEN:
            self.is_drawing = False
            self.mode = InteractionMode.IDLE

            if self.action_handler is not None:
                completed_stroke = (
                    self.action_handler.finish_stroke()
                )

                if (
                    completed_stroke is not None
                    and self.drawing_service is not None
                ):
                    self.drawing_service.add_stroke(
                        completed_stroke
                    )
