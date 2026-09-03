from app.application.canvas_coordinate_mapper import (
    CanvasCoordinateMapper,
)
from app.application.services.drawing_service import DrawingService
from app.application.services.hand_gesture_controller import (
    HandGestureController,
)
from app.application.services.interaction_action_handler import (
    InteractionActionHandler,
)
from app.core.enums.application_mode import ApplicationMode
from app.core.enums.hand_gesture import HandGesture
from app.core.enums.interaction_action import InteractionAction
from app.core.enums.interaction_zone import InteractionZone
from app.core.models.application_state import ApplicationState
from app.core.models.hand_gesture_event import HandGestureEvent
from app.core.models.point import Point
from app.core.models.profile import Profile

from app.storage.repositories.profile_repository import ProfileRepository

def test_fist_in_canvas_zone_starts_drawing():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=Point(960, 540),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.CANVAS
    assert action_handler.is_drawing is True


def test_open_in_color_ring_enters_color_selection():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(100, 540),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.COLOR_RING
    assert action_handler.mode.value == "color_selection"


def test_open_in_eraser_ring_enables_eraser():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(1820, 540),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.ERASER_RING
    assert action_handler.eraser_enabled is True


def test_open_in_undo_zone_requests_undo():
    class FakeHistoryManager:

        def __init__(self):
            self.undo_called = False

        def undo(self):
            self.undo_called = True

    history_manager = FakeHistoryManager()
    action_handler = InteractionActionHandler(
        history_manager=history_manager,
    )

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(480, 950),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.UNDO
    assert history_manager.undo_called is True


def test_open_in_redo_zone_requests_redo():
    class FakeHistoryManager:

        def __init__(self):
            self.redo_called = False

        def redo(self):
            self.redo_called = True

    history_manager = FakeHistoryManager()
    action_handler = InteractionActionHandler(
        history_manager=history_manager,
    )

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(1440, 950),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.REDO
    assert history_manager.redo_called is True


def test_open_in_canvas_zone_does_not_start_drawing():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    event = HandGestureEvent(
        gesture=HandGesture.OPEN,
        position=Point(960, 540),
    )

    controller.handle(event)

    assert controller.zone == InteractionZone.CANVAS
    assert action_handler.is_drawing is False


def test_controller_delegates_draw_action_to_handler():
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
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    point = Point(960, 540)

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=point,
    )

    controller.handle(event)

    assert action_handler.received_action == InteractionAction.DRAW
    assert action_handler.received_point == point


def test_fist_gesture_starts_stroke_and_adds_hand_position():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        action_handler=action_handler,
    )

    point = Point(500, 400)

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=point,
        )
    )

    assert action_handler.current_stroke is not None
    assert action_handler.current_stroke.points == [
        point,
    ]


def test_fist_gesture_builds_stroke_from_multiple_hand_positions():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        action_handler=action_handler,
    )

    first_point = Point(500, 400)
    second_point = Point(510, 410)
    third_point = Point(520, 420)

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=first_point,
        )
    )

    first_stroke = action_handler.current_stroke

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=second_point,
        )
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=third_point,
        )
    )

    assert action_handler.current_stroke is first_stroke
    assert action_handler.current_stroke.points == [
        first_point,
        second_point,
        third_point,
    ]


def test_fist_then_open_saves_completed_stroke_through_drawing_service():
    class SpyRepository:
        def __init__(self):
            self.saved_profiles = []

        def save(self, profile):
            self.saved_profiles.append(profile)

    repository = SpyRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    drawing_service = DrawingService(
        state=state,
        repository=repository,
    )

    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
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

    assert state.mode == ApplicationMode.DRAWING
    assert state.current_page.stroke_count == 1
    assert state.current_page.strokes[0].points == [
        point,
    ]
    assert repository.saved_profiles == [profile]


def test_open_without_points_does_not_send_empty_stroke_to_drawing_service():
    class SpyDrawingService:
        def __init__(self):
            self.received_strokes = []

        def add_stroke(self, stroke):
            self.received_strokes.append(stroke)

    action_handler = InteractionActionHandler()
    drawing_service = SpyDrawingService()

    controller = HandGestureController(
        action_handler=action_handler,
        drawing_service=drawing_service,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
        )
    )

    assert drawing_service.received_strokes == []


def test_multiple_fist_positions_are_saved_as_one_stroke():
    class SpyRepository:
        def __init__(self):
            self.saved_profiles = []

        def save(self, profile):
            self.saved_profiles.append(profile)

    repository = SpyRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    drawing_service = DrawingService(
        state=state,
        repository=repository,
    )

    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        action_handler=action_handler,
        drawing_service=drawing_service,
    )

    points = [
        Point(500, 400),
        Point(510, 410),
        Point(520, 420),
    ]

    for point in points:
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

    assert state.current_page.stroke_count == 1
    assert state.current_page.strokes[0].points == points
    assert repository.saved_profiles == [profile]


def test_controller_passes_canvas_local_position_to_action_handler():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    canvas_position = Point(
        x=672.0,
        y=378.0,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=canvas_position,
        )
    )

    assert action_handler.current_stroke is not None

    assert action_handler.current_stroke.points == [
        canvas_position,
    ]


def test_controller_maps_screen_position_to_canvas_position_before_drawing():
    canvas_mapper = CanvasCoordinateMapper(
        screen_width=1920,
        screen_height=1080,
        margin_ratio=0.15,
    )

    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
        canvas_coordinate_mapper=canvas_mapper,
    )

    screen_position = Point(
        x=960.0,
        y=540.0,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=screen_position,
        )
    )

    assert action_handler.current_stroke is not None

    assert action_handler.current_stroke.points == [
        Point(
            x=672.0,
            y=378.0,
        ),
    ]


def test_controller_does_not_map_position_when_hand_is_outside_canvas():
    class SpyCanvasCoordinateMapper:

        def __init__(self):
            self.received_positions = []

        def map(self, position):
            self.received_positions.append(
                position
            )

            return Point(
                x=999.0,
                y=999.0,
            )

    canvas_mapper = SpyCanvasCoordinateMapper()

    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
        canvas_coordinate_mapper=canvas_mapper,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=Point(
                x=100.0,
                y=540.0,
            ),
        )
    )

    assert controller.zone != InteractionZone.CANVAS

    assert canvas_mapper.received_positions == []


def test_open_gesture_finishes_stroke_when_position_is_present():
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=Point(
                x=960.0,
                y=540.0,
            ),
        )
    )

    assert action_handler.current_stroke is not None

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
            position=Point(
                x=960.0,
                y=540.0,
            ),
        )
    )

    assert action_handler.current_stroke is None
    assert action_handler.is_drawing is False
