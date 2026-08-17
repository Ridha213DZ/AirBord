from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class FaceIdentity:
    id: UUID = field(default_factory=uuid4)

    embedding: list[float] = field(
        default_factory=list
    )

    image_path: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def has_embedding(self) -> bool:
        return len(self.embedding) > 0