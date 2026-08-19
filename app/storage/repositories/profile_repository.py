from abc import ABC, abstractmethod
from typing import Optional

from app.core.models.profile import Profile


class ProfileRepository(ABC):
    """
    Abstract repository contract for Profile persistence.

    The rest of the application must depend on this
    interface, not on a specific storage implementation.

    Implementations may use:

        - JSON
        - SQLite
        - PostgreSQL
        - Remote API
        - Any other persistence mechanism
    """

    @abstractmethod
    def save(
        self,
        profile: Profile,
    ) -> None:
        """
        Create or update a profile.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        profile_id: str,
    ) -> Optional[Profile]:
        """
        Return a profile by its unique ID.

        Returns None if the profile does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_name(
        self,
        name: str,
    ) -> Optional[Profile]:
        """
        Return a profile by name.

        Returns None if no matching profile exists.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
    ) -> list[Profile]:
        """
        Return all profiles.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        profile_id: str,
    ) -> bool:
        """
        Delete a profile.

        Returns True if the profile existed and was deleted.
        Returns False if the profile does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        profile_id: str,
    ) -> bool:
        """
        Check whether a profile exists.
        """
        raise NotImplementedError