from uuid import uuid4

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


def test_drawing_service_adds_new_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    original_page = profile.current_page

    service = DrawingService(
        state=state,
        repository=repository,
    )

    new_page = service.add_page()

    assert new_page is profile.pages[-1]
    assert new_page is not original_page
    assert state.current_page is new_page
    assert len(profile.pages) == 2

    assert repository.saved_profiles == [profile]


def test_drawing_service_cannot_add_page_outside_drawing_mode():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.add_page()
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot add page outside drawing mode."
        )

    assert len(profile.pages) == 1
    assert state.current_page is profile.current_page
    assert repository.saved_profiles == []


def test_drawing_service_cannot_add_page_without_active_profile():
    repository = SpyProfileRepository()

    state = ApplicationState()

    state.mode = ApplicationMode.DRAWING
    state.current_profile = None
    state.current_page = None

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.add_page()
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot add page without an active profile."
        )

    assert state.current_profile is None
    assert state.current_page is None
    assert repository.saved_profiles == []


def test_drawing_service_removes_stroke_from_current_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    stroke = Stroke()

    state.current_page.add_stroke(stroke)

    service = DrawingService(
        state=state,
        repository=repository,
    )

    removed = service.remove_stroke(
        stroke.id
    )

    assert removed is True
    assert state.current_page.stroke_count == 0
    assert stroke not in state.current_page.strokes
    assert repository.saved_profiles == [profile]


def test_drawing_service_returns_false_when_stroke_does_not_exist():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    service = DrawingService(
        state=state,
        repository=repository,
    )
    removed = service.remove_stroke(
        uuid4()
    )

    assert removed is False
    assert state.current_page.stroke_count == 0
    assert repository.saved_profiles == []


def test_drawing_service_cannot_remove_stroke_outside_drawing_mode():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)

    stroke = Stroke()

    profile.current_page.add_stroke(stroke)

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.remove_stroke(
            stroke.id
        )
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot remove stroke outside drawing mode."
        )

    assert profile.current_page.stroke_count == 1
    assert repository.saved_profiles == []


def test_drawing_service_cannot_remove_stroke_without_active_profile():
    repository = SpyProfileRepository()

    state = ApplicationState()

    state.mode = ApplicationMode.DRAWING
    state.current_profile = None
    state.current_page = None

    service = DrawingService(
        state=state,
        repository=repository,
    )
    try:
        service.remove_stroke(uuid4())
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot remove stroke without an active profile."
        )

    assert state.current_profile is None
    assert state.current_page is None
    assert repository.saved_profiles == []


def test_drawing_service_cannot_remove_stroke_without_active_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.mode = ApplicationMode.DRAWING
    state.current_profile = profile
    state.current_page = None

    service = DrawingService(
        state=state,
        repository=repository,
    )
    try:
        service.remove_stroke(uuid4())
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot remove stroke without an active page."
        )
    assert state.current_profile is profile
    assert state.current_page is None
    assert repository.saved_profiles == []


def test_drawing_service_updates_existing_stroke():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    stroke = Stroke(
        color="#000000",
        width=5.0,
    )

    state.current_page.add_stroke(stroke)

    service = DrawingService(
        state=state,
        repository=repository,
    )

    updated = service.update_stroke(
        stroke.id,
        color="#FF0000",
        width=8.0,
    )

    assert updated is True
    assert stroke.color == "#FF0000"
    assert stroke.width == 8.0
    assert repository.saved_profiles == [profile]


def test_drawing_service_returns_false_when_updating_nonexistent_stroke():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    service = DrawingService(
        state=state,
        repository=repository,
    )

    updated = service.update_stroke(
        uuid4(),
        color="#FF0000",
        width=8.0,
    )

    assert updated is False
    assert state.current_page.stroke_count == 0
    assert repository.saved_profiles == []


def test_drawing_service_cannot_update_stroke_outside_drawing_mode():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)

    stroke = Stroke()

    profile.current_page.add_stroke(stroke)

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.update_stroke(
            stroke.id,
            color="#FF0000",
            width=8.0,
        )
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot update stroke outside drawing mode."
        )

    assert stroke.color == "#000000"
    assert stroke.width == 5.0
    assert repository.saved_profiles == []


def test_drawing_service_cannot_update_stroke_without_active_profile():
    repository = SpyProfileRepository()

    state = ApplicationState()

    state.mode = ApplicationMode.DRAWING
    state.current_profile = None
    state.current_page = None

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.update_stroke(
            uuid4(),
            color="#FF0000",
            width=8.0,
        )
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot update stroke without an active profile."
        )

    assert state.current_profile is None
    assert state.current_page is None
    assert repository.saved_profiles == []


def test_drawing_service_cannot_update_stroke_without_active_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.mode = ApplicationMode.DRAWING
    state.current_profile = profile
    state.current_page = None

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.update_stroke(
            uuid4(),
            color="#FF0000",
            width=8.0,
        )
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot update stroke without an active page."
        )

    assert state.current_profile is profile
    assert state.current_page is None
    assert repository.saved_profiles == []


def test_drawing_service_clears_current_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    page = state.current_page

    stroke_1 = Stroke()
    stroke_2 = Stroke()

    page.add_stroke(stroke_1)
    page.add_stroke(stroke_2)

    service = DrawingService(
        state=state,
        repository=repository,
    )

    cleared_page = service.clear_current_page()

    assert cleared_page is page
    assert state.current_page is page
    assert page.stroke_count == 0
    assert page.strokes == []
    assert repository.saved_profiles == [profile]


def test_drawing_service_does_not_save_when_current_page_is_empty():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)
    state.activate_drawing()

    page = state.current_page

    service = DrawingService(
        state=state,
        repository=repository,
    )

    cleared_page = service.clear_current_page()

    assert cleared_page is page
    assert page.stroke_count == 0
    assert repository.saved_profiles == []


def test_drawing_service_cannot_clear_current_page_outside_drawing_mode():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.activate_profile(profile)

    stroke = Stroke()

    profile.current_page.add_stroke(stroke)

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.clear_current_page()
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot clear current page outside drawing mode."
        )

    assert profile.current_page.stroke_count == 1
    assert repository.saved_profiles == []


def test_drawing_service_cannot_clear_current_page_without_active_profile():
    repository = SpyProfileRepository()

    state = ApplicationState()

    state.mode = ApplicationMode.DRAWING
    state.current_profile = None
    state.current_page = None

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.clear_current_page()
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot clear current page without an active profile."
        )

    assert state.current_profile is None
    assert state.current_page is None
    assert repository.saved_profiles == []


def test_drawing_service_cannot_clear_current_page_without_active_page():
    repository = SpyProfileRepository()

    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    state.mode = ApplicationMode.DRAWING
    state.current_profile = profile
    state.current_page = None

    service = DrawingService(
        state=state,
        repository=repository,
    )

    try:
        service.clear_current_page()
        assert False
    except RuntimeError as error:
        assert str(error) == (
            "Cannot clear current page without an active page."
        )

    assert state.current_profile is profile
    assert state.current_page is None
    assert repository.saved_profiles == []
