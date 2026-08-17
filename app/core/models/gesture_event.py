from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.core.enums.gesture_type import GestureType
from app.core.models.point import Point


@dataclass(frozen=True, slots=True)
class GestureEvent:
    type: GestureType

    position: Point | None = None

    confidence: float = 0.0

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )