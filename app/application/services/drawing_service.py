from uuid import UUID

from app.core.enums.application_mode import ApplicationMode
from app.core.models.application_state import ApplicationState
from app.core.models.page import Page
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


    def remove_stroke(
        self,
        stroke_id: UUID,
    ) -> bool:
        if self.state.mode != ApplicationMode.DRAWING:
            raise RuntimeError(
                "Cannot remove stroke outside drawing mode."
            )

        if self.state.current_profile is None:
            raise RuntimeError(
                "Cannot remove stroke without an active profile."
            )

        if self.state.current_page is None:
            raise RuntimeError(
                "Cannot remove stroke without an active page."
            )

        removed = self.state.current_page.remove_stroke(
            stroke_id
        )

        if not removed:
            return False

        self.state.current_profile.touch()

        self.repository.save(
            self.state.current_profile
        )

        return True

    def update_stroke(
        self,
        stroke_id: UUID,
        color: str,
        width: float,
    ) -> bool:
        if self.state.mode != ApplicationMode.DRAWING:
            raise RuntimeError(
                "Cannot update stroke outside drawing mode."
            )

        if self.state.current_profile is None:
            raise RuntimeError(
                "Cannot update stroke without an active profile."
            )

        if self.state.current_page is None:
            raise RuntimeError(
                "Cannot update stroke without an active page."
            )

        stroke = next(
            (
                stroke
                for stroke in self.state.current_page.strokes
                if stroke.id == stroke_id
            ),
            None,
        )

        if stroke is None:
            return False

        stroke.color = color
        stroke.width = width

        self.state.current_profile.touch()

        self.repository.save(
            self.state.current_profile
        )

        return True

    def clear_current_page(self) -> Page:
        if self.state.mode != ApplicationMode.DRAWING:
            raise RuntimeError(
                "Cannot clear current page outside drawing mode."
            )

        if self.state.current_profile is None:
            raise RuntimeError(
                "Cannot clear current page without an active profile."
            )

        if self.state.current_page is None:
            raise RuntimeError(
                "Cannot clear current page without an active page."
            )

        if self.state.current_page.stroke_count == 0:
            return self.state.current_page

        self.state.current_page.strokes.clear()

        self.state.current_profile.touch()

        self.repository.save(
            self.state.current_profile
        )

        return self.state.current_page


    def remove_current_page(self) -> Page:
        if self.state.mode != ApplicationMode.DRAWING:
            raise RuntimeError(
                "Cannot remove current page outside drawing mode."
            )

        if self.state.current_profile is None:
            raise RuntimeError(
                "Cannot remove current page without an active profile."
            )

        if self.state.current_page is None:
            raise RuntimeError(
                "Cannot remove current page without an active page."
            )

        if len(self.state.current_profile.pages) <= 1:
            page = self.state.current_page

            if page.stroke_count == 0:
                return page

            page.strokes.clear()
            page.touch()

            self.state.current_profile.touch()

            self.repository.save(
                self.state.current_profile
            )

            return page

        removed_page = self.state.current_profile.pages.pop()

        self.state.current_page = (
            self.state.current_profile.current_page
        )

        self.state.current_profile.touch()

        self.repository.save(
            self.state.current_profile
        )

        return removed_page


    def add_page(self):
        if self.state.mode != ApplicationMode.DRAWING:
            raise RuntimeError(
                "Cannot add page outside drawing mode."
            )
        if self.state.current_profile is None:
            raise RuntimeError(
                "Cannot add page without an active profile."
            )

        if self.state.current_page is None:
            raise RuntimeError(
                "Cannot add page without an active page."
            )

        page = self.state.current_profile.add_page()

        self.state.current_page = page

        self.repository.save(
            self.state.current_profile
        )

        return page