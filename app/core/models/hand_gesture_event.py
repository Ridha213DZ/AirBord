from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.core.enums.hand_gesture import HandGesture
from app.core.models.point import Point


@dataclass(frozen=True, slots=True)
class HandGestureEvent:
    gesture: HandGesture
    position: Point | None = None
    confidence: float = 0.0
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
