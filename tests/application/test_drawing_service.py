from app.application.services.drawing_service import (
    DrawingService,
)
from app.core.enums.application_mode import (
    ApplicationMode,
)
from app.core.models.application_state import (
    ApplicationState,
)
from app.core.models.point import Point
from app.core.models.profile import Profile
from app.core.models.stroke import Stroke
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


def test_drawing_service_adds_stroke_to_current_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    stroke = Stroke(
        color="#FF0000",
        width=8.0,
    )

    stroke.add_point(
        Point(
            x=10.0,
            y=20.0,
        )
    )

    service = DrawingService(
        state=state,
        repository=repository,
    )

    service.add_stroke(stroke)

    assert state.mode == ApplicationMode.DRAWING
    assert state.current_page is profile.current_page
    assert state.current_page.stroke_count == 1
    assert state.current_page.strokes[0] is stroke

    assert repository.saved_profiles == [profile]
def test_drawing_service_cannot_add_stroke_outside_drawing_mode():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)

    stroke = Stroke()

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.add_stroke(stroke)
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot draw outside drawing mode."
        )

    assert state.current_page.stroke_count == 0
    assert repository.saved_profiles == []
def test_drawing_service_cannot_add_stroke_without_active_profile():
    repository = SpyProfileRepository()

    state = ApplicationState()

    state.mode = ApplicationMode.DRAWING

    stroke = Stroke()

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.add_stroke(stroke)
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot draw without an active profile."
        )

    assert repository.saved_profiles == []


def test_drawing_service_cannot_add_stroke_without_active_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.current_profile = profile
    state.mode = ApplicationMode.DRAWING

    stroke = Stroke()

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.add_stroke(stroke)
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot draw without an active page."
        )

    assert profile.pages
    assert profile.current_page.stroke_count == 0
    assert repository.saved_profiles == []