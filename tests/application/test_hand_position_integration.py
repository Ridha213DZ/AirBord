from app.application.canvas_coordinate_mapper import (
    CanvasCoordinateMapper,
)
from app.application.hand_position_mapper import HandPositionMapper
from app.application.services.drawing_service import (
    DrawingService,
)
from app.application.services.hand_gesture_controller import (
    HandGestureController,
)
from app.application.services.interaction_action_handler import (
    InteractionActionHandler,
)

from app.core.enums.hand_gesture import HandGesture
from app.core.enums.interaction_zone import InteractionZone
from app.core.models.application_state import ApplicationState
from app.core.models.hand_gesture_event import HandGestureEvent
from app.core.models.point import Point
from app.core.models.profile import Profile

from app.storage.repositories.profile_repository import (
    ProfileRepository,
)


class SpyProfileRepository(ProfileRepository):

    def __init__(self) -> None:
        self.saved_profiles = []

    def save(self, profile):
        self.saved_profiles.append(profile)

    def get_by_id(self, profile_id):
        return None

    def get_by_name(self, name):
        return None

    def get_all(self):
        return []

    def delete(self, profile_id):
        return False

    def exists(self, profile_id):
        return False


def test_mapped_hand_position_reaches_canvas_and_starts_drawing():
    mapper = HandPositionMapper()
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    normalized_position = Point(
        x=0.5,
        y=0.5,
    )

    screen_position = mapper.map(
        position=normalized_position,
        width=1920,
        height=1080,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=screen_position,
        )
    )

    assert controller.zone == InteractionZone.CANVAS
    assert action_handler.is_drawing is True
    assert action_handler.current_stroke is not None
    assert action_handler.current_stroke.points == [
        Point(
            x=960.0,
            y=540.0,
        ),
    ]


def test_mapped_hand_position_in_left_15_percent_stays_outside_canvas():
    mapper = HandPositionMapper()
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    normalized_position = Point(
        x=0.05,
        y=0.5,
    )

    screen_position = mapper.map(
        position=normalized_position,
        width=1920,
        height=1080,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=screen_position,
        )
    )

    assert controller.zone == InteractionZone.COLOR_RING
    assert action_handler.is_drawing is False
    assert action_handler.current_stroke is None


def test_mapped_hand_position_in_right_15_percent_stays_outside_canvas():
    mapper = HandPositionMapper()
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1920,
        screen_height=1080,
        action_handler=action_handler,
    )

    normalized_position = Point(
        x=0.95,
        y=0.5,
    )

    screen_position = mapper.map(
        position=normalized_position,
        width=1920,
        height=1080,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=screen_position,
        )
    )

    assert controller.zone == InteractionZone.ERASER_RING
    assert action_handler.is_drawing is False
    assert action_handler.current_stroke is None


def test_mapped_hand_position_uses_target_screen_size_for_15_percent_zones():
    mapper = HandPositionMapper()
    action_handler = InteractionActionHandler()

    controller = HandGestureController(
        screen_width=1280,
        screen_height=720,
        action_handler=action_handler,
    )

    normalized_position = Point(
        x=0.05,
        y=0.5,
    )

    screen_position = mapper.map(
        position=normalized_position,
        width=1280,
        height=720,
    )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.FIST,
            position=screen_position,
        )
    )

    assert screen_position == Point(
        x=64.0,
        y=360.0,
    )

    assert controller.zone == InteractionZone.COLOR_RING
    assert action_handler.is_drawing is False
    assert action_handler.current_stroke is None


def test_normalized_hand_position_is_mapped_to_canvas_for_different_screen_size():
    hand_mapper = HandPositionMapper()
    canvas_mapper = CanvasCoordinateMapper(
        screen_width=1280,
        screen_height=720,
        margin_ratio=0.15,
    )

    normalized_position = Point(
        x=0.5,
        y=0.5,
    )

    screen_position = hand_mapper.map(
        position=normalized_position,
        width=1280,
        height=720,
    )

    canvas_position = canvas_mapper.map(
        screen_position
    )

    assert screen_position == Point(
        x=640.0,
        y=360.0,
    )

    assert canvas_position == Point(
        x=448.0,
        y=252.0,
    )


def test_normalized_hand_positions_create_canvas_local_stroke_in_page():
    hand_mapper = HandPositionMapper()

    canvas_mapper = CanvasCoordinateMapper(
        screen_width=1920,
        screen_height=1080,
        margin_ratio=0.15,
    )

    repository = SpyProfileRepository()

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
        canvas_coordinate_mapper=canvas_mapper,
    )

    normalized_positions = [
        Point(x=0.25, y=0.25),
        Point(x=0.50, y=0.50),
        Point(x=0.75, y=0.75),
    ]

    for normalized_position in normalized_positions:
        screen_position = hand_mapper.map(
            position=normalized_position,
            width=1920,
            height=1080,
        )

        controller.handle(
            HandGestureEvent(
                gesture=HandGesture.FIST,
                position=screen_position,
            )
        )

    controller.handle(
        HandGestureEvent(
            gesture=HandGesture.OPEN,
            position=Point(
                x=960.0,
                y=540.0,
            ),
        )
    )

    assert len(state.current_page.strokes) == 1

    assert state.current_page.strokes[0].points == [
        Point(x=192.0, y=108.0),
        Point(x=672.0, y=378.0),
        Point(x=1152.0, y=648.0),
    ]
