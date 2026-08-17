from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.models.point import Point


@dataclass
class Stroke:
    points: list[Point] = field(default_factory=list)

    color: str = "#000000"

    width: float = 5.0

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_point(self, point: Point) -> None:
        self.points.append(point)

    def is_empty(self) -> bool:
        return len(self.points) == 0