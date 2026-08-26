from uuid import UUID

from app.core.models.face_identity import FaceIdentity
from app.vision.face_recognition import FaceRecognition
from app.vision.models.detected_face import DetectedFace


class FakeFaceEncoder:

    def encode(self, frame, face):
        return [0.1, 0.2, 0.3]


class FakeFaceMatcher:

    def __init__(self, identity):
        self.identity = identity

    def match(self, embedding, identities):
        return self.identity


def test_face_recognition_matches_detected_face_to_identity():
    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    face = DetectedFace(
        x=100,
        y=80,
        width=200,
        height=200,
        confidence=0.95,
    )

    recognizer = FaceRecognition(
        encoder=FakeFaceEncoder(),
        matcher=FakeFaceMatcher(identity),
    )

    results = recognizer.recognize(
        frame=object(),
        faces=[face],
        identities=[identity],
    )

    assert len(results) == 1
    assert results[0].face is face
    assert results[0].identity is identity


def test_face_recognition_returns_unknown_when_no_identity_matches():
    class NoMatch:
        def encode(self, frame, face):
            return [0.9, 0.8, 0.7]

    class NoMatchMatcher:
        def match(self, embedding, identities):
            return None

    face = DetectedFace(
        x=100,
        y=80,
        width=200,
        height=200,
        confidence=0.95,
    )

    recognizer = FaceRecognition(
        encoder=NoMatch(),
        matcher=NoMatchMatcher(),
    )

    results = recognizer.recognize(
        frame=object(),
        faces=[face],
        identities=[],
    )

    assert len(results) == 1
    assert results[0].face is face
    assert results[0].identity is None
