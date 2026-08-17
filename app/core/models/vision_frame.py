from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class FrameSize:
    width: int
    height: int


@dataclass
class VisionFrame:
    timestamp: datetime

    frame_size: FrameSize

    face_detected: bool = False

    hand_detected: bool = False

    hand_landmarks: list[tuple[float, float]] | None = None

    @classmethod
    def create(
        cls,
        width: int,
        height: int,
    ) -> "VisionFrame":

        return cls(
            timestamp=datetime.now(timezone.utc),
            frame_size=FrameSize(
                width=width,
                height=height,
            ),
        )