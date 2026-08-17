from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.stroke import Stroke


@dataclass
class Page:
    id: UUID = field(default_factory=uuid4)

    strokes: list[Stroke] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_stroke(self, stroke: Stroke) -> None:
        self.strokes.append(stroke)
        self.touch()

    def remove_stroke(self, stroke_id: UUID) -> bool:
        original_count = len(self.strokes)

        self.strokes = [
            stroke
            for stroke in self.strokes
            if stroke.id != stroke_id
        ]

        changed = len(self.strokes) != original_count

        if changed:
            self.touch()

        return changed

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)

    @property
    def stroke_count(self) -> int:
        return len(self.strokes)