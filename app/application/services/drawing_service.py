from app.core.enums.application_mode import ApplicationMode
from app.core.models.application_state import ApplicationState
from app.core.models.stroke import Stroke
from app.storage.repositories.profile_repository import (
    ProfileRepository,
)


class DrawingService:
    """
    Application service responsible for drawing use cases.
    """

    def __init__(
        self,
        state: ApplicationState,
        repository: ProfileRepository,
    ) -> None:
        self.state = state
        self.repository = repository

    def add_stroke(
        self,
        stroke: Stroke,
    ) -> None:
        if self.state.mode != ApplicationMode.DRAWING:
            raise RuntimeError(
                "Cannot draw outside drawing mode."
            )

        if self.state.current_profile is None:
            raise RuntimeError(
                "Cannot draw without an active profile."
            )

        if self.state.current_page is None:
            raise RuntimeError(
                "Cannot draw without an active page."
            )

        self.state.current_page.add_stroke(
            stroke
        )

        self.state.current_profile.touch()

        self.repository.save(
            self.state.current_profile
        )