from app.application.services.hand_gesture_controller import HandGestureController
from app.core.enums.hand_gesture import HandGesture
from app.core.enums.interaction_action import InteractionAction
from app.core.enums.interaction_mode import InteractionMode
from app.core.enums.interaction_zone import InteractionZone
from app.core.models.hand_gesture_event import HandGestureEvent
from app.core.models.point import Point
from app.application.services.interaction_action_handler import (
    InteractionActionHandler,
)
from app.core.models.stroke import Stroke


def test_hand_gesture_controller_starts_in_idle_mode():
    controller = HandGestureController()

    assert controller.mode == InteractionMode.IDLE


def test_hand_gesture_controller_returns_to_idle_on_open():
    controller = HandGestureController()

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
        )
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
        )
    )

    assert controller.mode == InteractionMode.IDLE


def test_hand_gesture_controller_detects_canvas_zone_from_position():
    controller = HandGestureController()

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=Point(500, 400),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.CANVAS


def test_hand_gesture_controller_detects_canvas_zone_from_position():
    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
    )

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=Point(500, 400),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.CANVAS


def test_hand_gesture_controller_detects_color_ring_zone_from_position():
    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(100, 540),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.COLOR_RING


def test_hand_gesture_controller_uses_zone_detector():
    from app.application.services.hand_gesture_controller import (
        HandGestureController,
    )

    class FakeZoneDetector:

        def detect(self, position):
            return InteractionZone.COLOR_RING

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        zone_detector=FakeZoneDetector(),
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(500, 400),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.COLOR_RING


def test_hand_gesture_controller_uses_action_resolver():
    class FakeActionResolver:

        def __init__(self):
            self.received_gesture = None
            self.received_zone = None

        def resolve(self, gesture, zone):
            self.received_gesture = gesture
            self.received_zone = zone
            return None

    resolver = FakeActionResolver()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_resolver=resolver,
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(100, 540),
    )

    controller.handle(event)

    assert resolver.received_gesture == HandGesture.OPEN
    assert resolver.received_zone == InteractionZone.COLOR_RING


def test_hand_gesture_controller_passes_resolved_action_to_handler():
    class FakeActionResolver:

        def resolve(self, gesture, zone):
            return InteractionAction.DRAW

    class FakeActionHandler:

        def __init__(self):
            self.received_action = None
            self.received_point = None

        def handle(self, action):
            self.received_action = action

        def add_point(self, point):
            self.received_point = point

    action_handler = FakeActionHandler()

    controller = HandGestureController(
        action_resolver=FakeActionResolver(),
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=Point(500, 400),
    )

    controller.handle(event)

    assert action_handler.received_action == InteractionAction.DRAW


def test_hand_gesture_controller_adds_hand_position_to_current_stroke():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=Point(500, 400),
    )

    controller.handle(event)

    assert action_handler.current_stroke is not None
    assert action_handler.current_stroke.points == [
        Point(500, 400),
    ]


def test_hand_gesture_controller_passes_hand_position_to_action_handler():
    class FakeActionResolver:

        def resolve(self, gesture, zone):
            return InteractionAction.DRAW

    class FakeActionHandler:

        def __init__(self):
            self.received_action = None
            self.received_point = None

        def handle(self, action):
            self.received_action = action

        def add_point(self, point):
            self.received_point = point

    action_handler = FakeActionHandler()

    controller = HandGestureController(
        action_resolver=FakeActionResolver(),
        action_handler=action_handler,
    )

    point = Point(500, 400)

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=point,
    )

    controller.handle(event)

    assert action_handler.received_action == InteractionAction.DRAW
    assert action_handler.received_point == point


def test_hand_gesture_controller_open_stops_drawing_and_clears_current_stroke():
    action_handler = InteractionActionHandler()

    class FakeActionResolver:
        def resolve(self, gesture, zone):
            if gesture == HandGesture.FIST:
                return InteractionAction.DRAW

            return None

    controller = HandGestureController(
        action_resolver=FakeActionResolver(),
        action_handler=action_handler,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=Point(500, 400),
        )
    )

    assert controller.is_drawing is True
    assert action_handler.is_drawing is True
    assert action_handler.current_stroke is not None

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
            position=Point(500, 400),
        )
    )

    assert controller.is_drawing is False
    assert controller.mode == InteractionMode.IDLE
    assert action_handler.is_drawing is False
    assert action_handler.current_stroke is None


def test_hand_gesture_controller_open_finishes_current_stroke():
    action_handler = InteractionActionHandler()

    class FakeActionResolver:
        def resolve(self, gesture, zone):
            if gesture == HandGesture.FIST:
                return InteractionAction.DRAW

            return None

    controller = HandGestureController(
        action_resolver=FakeActionResolver(),
        action_handler=action_handler,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=Point(500, 400),
        )
    )

    assert controller.is_drawing is True
    assert action_handler.current_stroke is not None

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
        )
    )

    assert controller.is_drawing is False
    assert action_handler.is_drawing is False
    assert action_handler.current_stroke is None


def test_hand_gesture_controller_open_finishes_stroke_through_handler():
    class FakeActionHandler:
        def __init__(self):
            self.finished = False

        def handle(self, action):
            pass

        def add_point(self, point):
            pass

        def finish_stroke(self):
            self.finished = True

    action_handler = FakeActionHandler()

    controller = HandGestureController(
        action_handler=action_handler,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
        )
    )

    assert action_handler.finished is True


def test_hand_gesture_controller_saves_completed_stroke_through_drawing_service():
    class FakeActionHandler:
        def __init__(self):
            self.finished_stroke = Stroke()

        def handle(self, action):
            pass

        def add_point(self, point):
            self.finished_stroke.add_point(point)

        def finish_stroke(self):
            return self.finished_stroke

    class FakeDrawingService:
        def __init__(self):
            self.received_stroke = None

        def add_stroke(self, stroke):
            self.received_stroke = stroke

    action_handler = FakeActionHandler()
    drawing_service = FakeDrawingService()

    controller = HandGestureController(
        action_handler=action_handler,
        drawing_service=drawing_service,
    )

    point = Point(500, 400)

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=point,
        )
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
        )
    )

    assert drawing_service.received_stroke is action_handler.finished_stroke


def test_hand_gesture_controller_does_not_save_when_no_stroke_is_finished():
    class FakeActionHandler:
        def handle(self, action):
            pass

        def finish_stroke(self):
            return None

    class FakeDrawingService:
        def __init__(self):
            self.add_stroke_called = False

        def add_stroke(self, stroke):
            self.add_stroke_called = True

    action_handler = FakeActionHandler()
    drawing_service = FakeDrawingService()

    controller = HandGestureController(
        action_handler=action_handler,
        drawing_service=drawing_service,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
        )
    )

    assert drawing_service.add_stroke_called is False
