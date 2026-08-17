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
    assert not frame.face_detected
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