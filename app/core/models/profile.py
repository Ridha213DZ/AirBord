from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.face_identity import FaceIdentity
from app.core.models.page import Page


@dataclass
class Profile:
    id: UUID = field(default_factory=uuid4)

    name: str = ""

    face_identity: FaceIdentity | None = None

    pages: list[Page] = field(
        default_factory=list
    )

    current_page_index: int = 0

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if not self.pages:
            self.pages.append(Page())

        if self.current_page_index >= len(self.pages):
            self.current_page_index = len(self.pages) - 1

    @property
    def current_page(self) -> Page:
        return self.pages[
            self.current_page_index
        ]

    def add_page(self) -> Page:
        page = Page()

        self.pages.append(page)

        self.current_page_index = (
            len(self.pages) - 1
        )

        self.touch()

        return page

    def move_to_previous_page(self) -> bool:
        if self.current_page_index == 0:
            return False

        self.current_page_index -= 1

        return True

    def move_to_next_page(self) -> bool:
        if (
            self.current_page_index
            >= len(self.pages) - 1
        ):
            return False

        self.current_page_index += 1

        return True

    def remove_current_page(self) -> Page | None:
        if len(self.pages) <= 1:
            return None

        removed_page = self.pages.pop(
            self.current_page_index
        )

        if self.current_page_index >= len(self.pages):
            self.current_page_index = (
                len(self.pages) - 1
            )

        self.touch()

        return removed_page

    def touch(self) -> None:
        self.updated_at = datetime.now(
            timezone.utc
        )
