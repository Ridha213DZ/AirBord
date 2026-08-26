from app.core.models.face_identity import FaceIdentity
from app.vision.face_matcher import FaceMatcher


def test_face_matcher_returns_matching_face_identity():
    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    matcher = FaceMatcher()

    matched = matcher.match(
        embedding=[0.1, 0.2, 0.3],
        identities=[identity],
    )

    assert matched is identity


def test_face_matcher_returns_none_when_no_identity_matches():
    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    matcher = FaceMatcher()

    matched = matcher.match(
        embedding=[0.9, 0.8, 0.7],
        identities=[identity],
    )

    assert matched is None


def test_face_matcher_returns_closest_identity():
    first_identity = FaceIdentity(
        embedding=[0.0, 0.0],
    )

    second_identity = FaceIdentity(
        embedding=[1.0, 1.0],
    )

    matcher = FaceMatcher()

    matched = matcher.match(
        embedding=[0.1, 0.1],
        identities=[
            first_identity,
            second_identity,
        ],
    )

    assert matched is first_identity


def test_face_matcher_ignores_identity_without_embedding():
    identity_without_embedding = FaceIdentity()

    valid_identity = FaceIdentity(
        embedding=[0.1, 0.1],
    )

    matcher = FaceMatcher()

    matched = matcher.match(
        embedding=[0.1, 0.1],
        identities=[
            identity_without_embedding,
            valid_identity,
        ],
    )

    assert matched is valid_identity
