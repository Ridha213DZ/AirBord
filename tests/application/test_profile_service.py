import pytest

from app.core.enums.application_mode import ApplicationMode
from app.core.models.application_state import ApplicationState
from app.application.services.profile_service import ProfileService
from app.core.models.face_identity import FaceIdentity
from app.core.models.profile import Profile


class FakeProfileRepository:
    """
    In-memory repository used only for
    testing the application service.
    """

    def __init__(self):
        self.profiles = {}

    def save(
        self,
        profile: Profile,
    ) -> None:
        self.profiles[
            str(profile.id)
        ] = profile

    def get_by_id(
        self,
        profile_id,
    ) -> Profile | None:
        return self.profiles.get(
            str(profile_id)
        )

    def get_by_name(
        self,
        name: str,
    ) -> Profile | None:
        for profile in self.profiles.values():
            if profile.name == name:
                return profile

        return None

    def get_all(
        self,
    ) -> list[Profile]:
        return list(
            self.profiles.values()
        )

    def delete(
        self,
        profile_id,
    ) -> bool:
        profile_id = str(
            profile_id
        )

        if profile_id not in self.profiles:
            return False

        del self.profiles[
            profile_id
        ]

        return True

    def exists(
        self,
        profile_id,
    ) -> bool:
        return (
            str(profile_id)
            in self.profiles
        )


@pytest.fixture
def repository():
    return FakeProfileRepository()


@pytest.fixture
def service(repository):
    return ProfileService(
        repository=repository,
        state=ApplicationState(),
    )


def test_create_profile(
    service,
):
    profile = service.create_profile(
        name="Ridha"
    )

    assert profile.name == "Ridha"


def test_create_profile_saves_profile(
    service,
    repository,
):
    profile = service.create_profile(
        name="Ridha"
    )

    assert repository.exists(
        profile.id
    )


def test_get_profile_by_id(
    service,
):
    created = service.create_profile(
        name="Ridha"
    )

    loaded = service.get_profile(
        created.id
    )

    assert loaded is not None
    assert loaded.id == created.id


def test_get_unknown_profile_returns_none(
    service,
):
    profile = service.get_profile(
        "unknown-profile"
    )

    assert profile is None


def test_get_profile_by_name(
    service,
):
    created = service.create_profile(
        name="Ridha"
    )

    loaded = service.get_profile_by_name(
        "Ridha"
    )

    assert loaded is not None
    assert loaded.id == created.id


def test_get_all_profiles(
    service,
):
    service.create_profile(
        name="Ridha"
    )

    service.create_profile(
        name="Haytham"
    )

    profiles = service.get_all_profiles()

    assert len(
        profiles
    ) == 2


def test_rename_profile(
    service,
):
    profile = service.create_profile(
        name="Ridha"
    )

    updated = service.rename_profile(
        profile.id,
        "Ridha Berrehouma",
    )

    assert updated is not None

    assert updated.name == (
        "Ridha Berrehouma"
    )

    loaded = service.get_profile(
        profile.id
    )

    assert loaded.name == (
        "Ridha Berrehouma"
    )


def test_rename_unknown_profile_returns_none(
    service,
):
    updated = service.rename_profile(
        "unknown-profile",
        "Someone",
    )

    assert updated is None


def test_delete_profile(
    service,
):
    profile = service.create_profile(
        name="Ridha"
    )

    deleted = service.delete_profile(
        profile.id
    )

    assert deleted is True

    assert service.get_profile(
        profile.id
    ) is None


def test_delete_unknown_profile_returns_false(
    service,
):
    deleted = service.delete_profile(
        "unknown-profile"
    )

    assert deleted is False


def test_assign_face_identity(
    service,
):
    profile = service.create_profile(
        name="Ridha"
    )

    face_identity = FaceIdentity(
        embedding=[
            0.1,
            0.2,
            0.3,
        ]
    )

    updated = service.assign_face_identity(
        profile.id,
        face_identity,
    )

    assert updated is not None

    assert (
        updated.face_identity
        is not None
    )

    assert (
        updated.face_identity.id
        == face_identity.id
    )


def test_assign_face_identity_to_unknown_profile_returns_none(
    service,
):
    face_identity = FaceIdentity()

    updated = service.assign_face_identity(
        "unknown-profile",
        face_identity,
    )

    assert updated is None


def test_create_and_activate_profile(
    repository,
):
    state = ApplicationState()

    service = ProfileService(
        repository=repository,
        state=state,
    )

    profile = service.create_and_activate_profile(
        name="Ridha"
    )

    assert profile.name == "Ridha"
    assert repository.exists(profile.id)

    assert state.current_profile is profile
    assert state.current_page is profile.current_page
    assert state.mode == ApplicationMode.PROFILE_ACTIVE


def test_activate_existing_profile(
    repository,
):
    state = ApplicationState()

    profile = Profile(
        name="Ridha"
    )

    repository.save(
        profile
    )

    service = ProfileService(
        repository=repository,
        state=state,
    )

    activated = service.activate_profile(
        profile.id
    )

    assert activated is profile

    assert state.current_profile is profile
    assert state.current_page is profile.current_page

    assert (
        state.mode
        == ApplicationMode.PROFILE_ACTIVE
    )


def test_activate_unknown_profile_returns_none_without_changing_state(
    repository,
):
    state = ApplicationState()

    service = ProfileService(
        repository=repository,
        state=state,
    )

    activated = service.activate_profile(
        "unknown-profile"
    )

    assert activated is None
    assert state.current_profile is None
    assert state.current_page is None
    assert state.mode == ApplicationMode.IDLE


def test_activate_profile_by_face_identity(
    repository,
):
    state = ApplicationState()

    face_identity = FaceIdentity(
        embedding=[
            0.1,
            0.2,
            0.3,
        ]
    )

    profile = Profile(
        name="Ridha",
        face_identity=face_identity,
    )

    repository.save(
        profile
    )

    service = ProfileService(
        repository=repository,
        state=state,
    )

    activated = service.activate_profile_by_face_identity(
        face_identity.id
    )

    assert activated is profile
    assert state.current_profile is profile
    assert state.current_page is profile.current_page
    assert state.mode == ApplicationMode.PROFILE_ACTIVE


def test_activate_profile_by_unknown_face_identity_returns_none_without_changing_state(
    repository,
):
    state = ApplicationState()

    profile = Profile(
        name="Ridha",
        face_identity=FaceIdentity(
            embedding=[
                0.1,
                0.2,
                0.3,
            ]
        ),
    )

    repository.save(
        profile
    )

    service = ProfileService(
        repository=repository,
        state=state,
    )

    unknown_face_identity = FaceIdentity(
        embedding=[
            0.9,
            0.8,
            0.7,
        ]
    )

    activated = service.activate_profile_by_face_identity(
        unknown_face_identity.id
    )

    assert activated is None
    assert state.current_profile is None
    assert state.current_page is None
    assert state.mode == ApplicationMode.IDLE
