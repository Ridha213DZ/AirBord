import json
from pathlib import Path
from uuid import UUID

from app.core.models.profile import Profile
from app.storage.repositories.profile_repository import (
    ProfileRepository,
)
from app.storage.serializers.profile_serializer import (
    ProfileSerializer,
)


class JsonProfileRepository(ProfileRepository):
    """
    JSON file implementation of ProfileRepository.

    Profiles are stored in a single JSON file.
    """

    def __init__(
        self,
        storage_file: Path,
    ) -> None:
        self.storage_file = Path(
            storage_file
        )

        self.serializer = ProfileSerializer()

        self._ensure_storage_file()

    # ----------------------------------------
    # Public API
    # ----------------------------------------

    def save(
        self,
        profile: Profile,
    ) -> None:
        profiles = self._load_all()

        serialized_profile = (
            self.serializer.to_dict(
                profile
            )
        )

        profile_id = str(
            profile.id
        )

        updated = False

        for index, stored_profile in enumerate(
            profiles
        ):
            if (
                stored_profile.get("id")
                == profile_id
            ):
                profiles[index] = (
                    serialized_profile
                )

                updated = True

                break

        if not updated:
            profiles.append(
                serialized_profile
            )

        self._write_all(
            profiles
        )

    def get_by_id(
        self,
        profile_id: UUID | str,
    ) -> Profile | None:
        profile_id = str(
            profile_id
        )

        profiles = self._load_all()

        for stored_profile in profiles:
            if (
                stored_profile.get("id")
                == profile_id
            ):
                return (
                    self.serializer.from_dict(
                        stored_profile
                    )
                )

        return None

    def get_by_name(
        self,
        name: str,
    ) -> Profile | None:
        profiles = self._load_all()

        for stored_profile in profiles:
            if (
                stored_profile.get("name")
                == name
            ):
                return (
                    self.serializer.from_dict(
                        stored_profile
                    )
                )

        return None

    def get_all(
        self,
    ) -> list[Profile]:
        profiles = self._load_all()

        return [
            self.serializer.from_dict(
                stored_profile
            )
            for stored_profile in profiles
        ]

    def delete(
        self,
        profile_id: UUID | str,
    ) -> bool:
        profile_id = str(
            profile_id
        )

        profiles = self._load_all()

        remaining_profiles = [
            profile
            for profile in profiles
            if (
                profile.get("id")
                != profile_id
            )
        ]

        deleted = (
            len(remaining_profiles)
            != len(profiles)
        )

        if deleted:
            self._write_all(
                remaining_profiles
            )

        return deleted

    def exists(
        self,
        profile_id: UUID | str,
    ) -> bool:
        return (
            self.get_by_id(
                profile_id
            )
            is not None
        )

    # ----------------------------------------
    # Storage management
    # ----------------------------------------

    def _ensure_storage_file(
        self,
    ) -> None:
        self.storage_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.storage_file.exists():
            self._write_all(
                []
            )

    def _load_all(
        self,
    ) -> list[dict]:
        try:
            with self.storage_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(
                    file
                )

        except (
            FileNotFoundError,
            json.JSONDecodeError,
        ):
            return []

        if not isinstance(
            data,
            list,
        ):
            return []

        return data

    def _write_all(
        self,
        profiles: list[dict],
    ) -> None:
        with self.storage_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                profiles,
                file,
                ensure_ascii=False,
                indent=4,
            )