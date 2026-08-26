from uuid import uuid4

from app.vision.models.recognition_result import (
    RecognitionResult,
)


def test_recognition_result_contains_identity_and_confidence():
    face_identity_id = uuid4()

    result = RecognitionResult(
        face_identity_id=face_identity_id,
        confidence=0.93,
    )

    assert result.face_identity_id == face_identity_id
    assert result.confidence == 0.93
