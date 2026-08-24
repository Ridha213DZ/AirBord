from uuid import UUID

from app.core.models.application_state import ApplicationState
from app.core.models.face_identity import FaceIdentity
from app.core.models.profile import Profile
from app.storage.repositories.profile_repository import (
    ProfileRepository,
)


class ProfileService:
    """
    Application service responsible for profile use cases.

    The service coordinates domain objects and the repository,
    without knowing how profiles are physically stored.
    """

    def __init__(
        self,
        repository: ProfileRepository,
        state: ApplicationState,
    ) -> None:
        self.repository = repository
        self.state = state

    def create_profile(
        self,
        name: str,
    ) -> Profile:
        profile = Profile(
            name=name,
        )

        self.repository.save(
            profile
        )

        return profile

    def get_profile(
        self,
        profile_id: UUID | str,
    ) -> Profile | None:
        return self.repository.get_by_id(
        profile_id
        )

    def get_profile_by_name(
        self,
        name: str,
    ) -> Profile | None:
        return self.repository.get_by_name(
            name
        )

    def get_all_profiles(
        self,
    ) -> list[Profile]:
        return self.repository.get_all()

    def rename_profile(
        self,
        profile_id: UUID | str,
        name: str,
    ) -> Profile | None:
        profile = self.repository.get_by_id(
            profile_id
        )

        if profile is None:
            return None

        profile.name = name

        profile.touch()

        self.repository.save(
            profile
        )

        return profile

    def delete_profile(
        self,
        profile_id: UUID | str,
    ) -> bool:
        return self.repository.delete(
            profile_id
        )

    def assign_face_identity(
        self,
        profile_id: UUID | str,
        face_identity: FaceIdentity,
    ) -> Profile | None:
        profile = self.repository.get_by_id(
            profile_id
        )

        if profile is None:
            return None

        profile.face_identity = face_identity

        profile.touch()

        self.repository.save(
            profile
        )

        return profile

    def create_and_activate_profile(
        self,
        name: str,
    ) -> Profile:
        profile = self.create_profile(
            name
        )

        self.state.activate_profile(
            profile
        )

        return profile

    def activate_profile(
        self,
        profile_id: UUID | str,
    ) -> Profile | None:
        profile = self.repository.get_by_id(
            profile_id
        )

        if profile is None:
            return None

        self.state.activate_profile(
            profile
        )

        return profile
