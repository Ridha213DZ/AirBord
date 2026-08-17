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

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if not self.pages:
            self.pages.append(Page())

    @property
    def current_page(self) -> Page:
        return self.pages[-1]

    def add_page(self) -> Page:
        page = Page()

        self.pages.append(page)

        self.touch()

        return page

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)