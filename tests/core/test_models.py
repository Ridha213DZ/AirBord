from uuid import UUID

from app.core.enums.application_mode import ApplicationMode
from app.core.enums.gesture_type import GestureType
from app.core.models.application_state import ApplicationState
from app.core.models.drawing_settings import DrawingSettings
from app.core.models.face_identity import FaceIdentity
from app.core.models.gesture_event import GestureEvent
from app.core.models.page import Page
from app.core.models.point import Point
from app.core.models.profile import Profile
from app.core.models.stroke import Stroke
from app.core.models.vision_frame import FrameSize, VisionFrame


def test_point():

    point = Point(
        x=10.5,
        y=20.25,
    )

    assert point.x == 10.5
    assert point.y == 20.25


def test_point_is_immutable():

    point = Point(
        x=10,
        y=20,
    )

    try:
        point.x = 100
        assert False
    except AttributeError:
        assert True


def test_stroke():

    stroke = Stroke(
        color="#ff0000",
        width=8.0,
    )

    stroke.add_point(
        Point(10, 20)
    )

    stroke.add_point(
        Point(15, 25)
    )

    assert isinstance(stroke.id, UUID)
    assert len(stroke.points) == 2
    assert stroke.color == "#ff0000"
    assert stroke.width == 8.0
    assert not stroke.is_empty()


def test_page():

    page = Page()

    stroke = Stroke()

    page.add_stroke(stroke)

    assert isinstance(page.id, UUID)
    assert page.stroke_count == 1
    assert page.strokes[0] is stroke


def test_profile_creates_first_page():

    profile = Profile(
        name="Ahmed"
    )

    assert isinstance(profile.id, UUID)
    assert profile.name == "Ahmed"

    assert len(profile.pages) == 1
    assert isinstance(
        profile.current_page,
        Page,
    )


def test_profile_can_add_page():

    profile = Profile(
        name="Ahmed"
    )

    first_page = profile.current_page

    second_page = profile.add_page()

    assert len(profile.pages) == 2
    assert second_page is profile.pages[1]
    assert second_page is not first_page


def test_face_identity():

    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
        image_path="profiles/face.jpg",
    )

    assert isinstance(identity.id, UUID)
    assert identity.has_embedding()
    assert identity.image_path == "profiles/face.jpg"


def test_drawing_settings():

    settings = DrawingSettings(
        color="#00ff00",
        brush_size=10,
    )

    assert settings.color == "#00ff00"
    assert settings.brush_size == 10
    assert not settings.eraser_enabled

    settings.enable_eraser()

    assert settings.eraser_enabled

    settings.disable_eraser()

    assert not settings.eraser_enabled


def test_gesture_event():

    event = GestureEvent(
        type=GestureType.DRAW_START,
        position=Point(100, 200),
        confidence=0.95,
    )

    assert event.type == GestureType.DRAW_START
    assert event.position == Point(100, 200)
    assert event.confidence == 0.95


def test_vision_frame():

    frame = VisionFrame.create(
        width=640,
        height=480,
    )

    assert isinstance(
        frame.frame_size,
        FrameSize,
    )

    assert frame.frame_size.width == 640
    assert frame.frame_size.height == 480
    assert not frame.hand_detected


def test_application_state():

    state = ApplicationState()

    assert state.mode == ApplicationMode.IDLE
    assert state.current_profile is None
    assert state.current_page is None


def test_application_state_profile_activation():

    state = ApplicationState()

    profile = Profile(
        name="Ahmed"
    )

    state.activate_profile(profile)

    assert state.current_profile is profile
    assert state.current_page is profile.current_page
    assert state.mode == ApplicationMode.PROFILE_ACTIVE


def test_application_state_drawing_activation():

    state = ApplicationState()

    profile = Profile(
        name="Ahmed"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    assert state.mode == ApplicationMode.DRAWING


def test_application_state_cannot_draw_without_profile():

    state = ApplicationState()

    try:
        state.activate_drawing()
        assert False
    except RuntimeError:
        assert True


def test_profile_starts_with_first_page_as_current():
    profile = Profile(
        name="Ridha"
    )

    assert profile.current_page_index == 0
    assert profile.current_page is profile.pages[0]


def test_profile_add_page_makes_new_page_current():
    profile = Profile(
        name="Ridha"
    )

    first_page = profile.current_page

    new_page = profile.add_page()

    assert profile.pages == [
        first_page,
        new_page,
    ]
    assert profile.current_page_index == 1
    assert profile.current_page is new_page


def test_profile_can_move_to_previous_page():
    profile = Profile(
        name="Ridha"
    )

    first_page = profile.current_page
    second_page = profile.add_page()

    moved = profile.move_to_previous_page()

    assert moved is True
    assert profile.current_page_index == 0
    assert profile.current_page is first_page
    assert profile.current_page is not second_page


def test_profile_can_move_to_next_page():
    profile = Profile(
        name="Ridha"
    )

    profile.add_page()

    first_page = profile.move_to_previous_page()

    assert first_page is True

    moved = profile.move_to_next_page()

    assert moved is True
    assert profile.current_page_index == 1
    assert profile.current_page is profile.pages[1]


def test_profile_cannot_move_before_first_page():
    profile = Profile(
        name="Ridha"
    )

    moved = profile.move_to_previous_page()

    assert moved is False
    assert profile.current_page_index == 0


def test_profile_cannot_move_after_last_page():
    profile = Profile(
        name="Ridha"
    )

    moved = profile.move_to_next_page()

    assert moved is False
    assert profile.current_page_index == 0


def test_profile_removes_current_middle_page_and_keeps_index():
    profile = Profile(
        name="Ridha"
    )

    first_page = profile.current_page
    second_page = profile.add_page()
    third_page = profile.add_page()

    profile.move_to_previous_page()

    removed_page = profile.remove_current_page()

    assert removed_page is second_page
    assert profile.pages == [
        first_page,
        third_page,
    ]
    assert profile.current_page_index == 1
    assert profile.current_page is third_page


def test_profile_removes_last_page_and_moves_to_previous_page():
    profile = Profile(
        name="Ridha"
    )

    first_page = profile.current_page
    second_page = profile.add_page()

    removed_page = profile.remove_current_page()

    assert removed_page is second_page
    assert profile.pages == [
        first_page,
    ]
    assert profile.current_page_index == 0
    assert profile.current_page is first_page


def test_profile_cannot_remove_only_page():
    profile = Profile(
        name="Ridha"
    )

    page = profile.current_page

    removed_page = profile.remove_current_page()

    assert removed_page is None
    assert profile.pages == [
        page,
    ]
    assert profile.current_page_index == 0
    assert profile.current_page is page


def test_profile_clamps_current_page_index_to_last_page():
    first_page = Page()
    second_page = Page()

    profile = Profile(
        name="Ridha",
        pages=[
            first_page,
            second_page,
        ],
        current_page_index=10,
    )

    assert profile.current_page_index == 1
    assert profile.current_page is second_page


def test_profile_add_page_updates_updated_at():
    profile = Profile(
        name="Ridha",
    )

    previous_updated_at = profile.updated_at

    profile.add_page()

    assert profile.updated_at >= previous_updated_at


def test_profile_remove_current_page_updates_updated_at():
    profile = Profile(
        name="Ridha",
    )

    profile.add_page()

    previous_updated_at = profile.updated_at

    profile.remove_current_page()

    assert profile.updated_at >= previous_updated_at


def test_application_state_clear_profile_resets_state():
    state = ApplicationState()

    profile = Profile(
        name="Ridha",
    )

    state.activate_profile(
        profile
    )

    state.active_gesture = GestureEvent(
    type=GestureType.DRAW_START
    )

    state.clear_profile()

    assert state.current_profile is None
    assert state.current_page is None
    assert state.active_gesture is None
    assert state.mode == ApplicationMode.IDLE


def test_application_state_activate_drawing_restores_current_page():
    state = ApplicationState()

    profile = Profile(
        name="Ridha",
    )

    state.activate_profile(
        profile
    )

    state.current_page = None

    state.activate_drawing()

    assert state.current_page is profile.current_page
    assert state.mode == ApplicationMode.DRAWING


def test_page_add_stroke_updates_updated_at():
    page = Page()

    previous_updated_at = page.updated_at

    stroke = Stroke()

    page.add_stroke(
        stroke
    )

    assert page.updated_at > previous_updated_at


def test_page_remove_stroke():
    page = Page()

    stroke = Stroke()

    page.add_stroke(
        stroke
    )

    removed = page.remove_stroke(
        stroke.id
    )

    assert removed is True
    assert page.stroke_count == 0
    assert stroke not in page.strokes


def test_page_remove_unknown_stroke_returns_false():
    page = Page()

    unknown_stroke = Stroke()

    removed = page.remove_stroke(
        unknown_stroke.id
    )

    assert removed is False
    assert page.stroke_count == 0


def test_page_remove_stroke_updates_updated_at():
    page = Page()

    stroke = Stroke()

    page.add_stroke(
        stroke
    )

    previous_updated_at = page.updated_at

    page.remove_stroke(
        stroke.id
    )

    assert page.updated_at > previous_updated_at


def test_face_identity_has_embedding():
    identity = FaceIdentity(
        embedding=[
            0.1,
            0.2,
            0.3,
        ]
    )

    assert identity.has_embedding() is True


def test_face_identity_has_no_embedding():
    identity = FaceIdentity()

    assert identity.has_embedding() is False


def test_stroke_is_empty_when_created():
    stroke = Stroke()

    assert stroke.is_empty() is True


def test_vision_frame_starts_without_hand_landmarks():
    frame = VisionFrame.create(
        width=640,
        height=480,
    )

    assert frame.hand_landmarks is None


def test_gesture_event_has_timestamp():
    event = GestureEvent(
        type=GestureType.DRAW_START,
    )

    assert event.timestamp is not None


def test_gesture_event_timestamp_is_utc():
    event = GestureEvent(
        type=GestureType.DRAW_START,
    )

    assert event.timestamp.tzinfo is not None
    assert event.timestamp.utcoffset().total_seconds() == 0


def test_drawing_settings_enable_eraser_is_idempotent():
    settings = DrawingSettings()

    settings.enable_eraser()
    settings.enable_eraser()

    assert settings.eraser_enabled is True
