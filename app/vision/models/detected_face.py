from dataclasses import dataclass


@dataclass
class DetectedFace:
    x: int
    y: int
    width: int
    height: int
    confidence: float
