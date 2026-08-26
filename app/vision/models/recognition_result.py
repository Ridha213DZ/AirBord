from dataclasses import dataclass
from uuid import UUID


@dataclass
class RecognitionResult:
    face_identity_id: UUID
    confidence: float
