from app.vision.models.detected_face import DetectedFace
from app.vision.face_selector import FaceSelector


def test_face_selector_selects_largest_face():
    faces = [
        DetectedFace(
            x=100,
            y=100,
            width=80,
            height=80,
            confidence=0.95,
        ),
        DetectedFace(
            x=300,
            y=100,
            width=200,
            height=200,
            confidence=0.90,
        ),
    ]

    selector = FaceSelector()

    selected = selector.select(
        faces
    )

    assert selected is faces[1]


def test_face_selector_returns_none_when_no_faces():
    selector = FaceSelector()

    selected = selector.select([])

    assert selected is None


def test_face_selector_prefers_face_inside_target_region():
    faces = [
        DetectedFace(
            x=50,
            y=50,
            width=200,
            height=200,
            confidence=0.95,
        ),
        DetectedFace(
            x=280,
            y=180,
            width=100,
            height=100,
            confidence=0.90,
        ),
    ]

    target_region = (
        250,
        150,
        200,
        200,
    )

    selector = FaceSelector()

    selected = selector.select(
        faces,
        target_region=target_region,
    )

    assert selected is faces[1]


def test_face_selector_returns_none_when_no_face_is_inside_target_region():
    faces = [
        DetectedFace(
            x=50,
            y=50,
            width=80,
            height=80,
            confidence=0.95,
        ),
    ]

    target_region = (
        300,
        200,
        200,
        200,
    )

    selector = FaceSelector()

    selected = selector.select(
        faces,
        target_region=target_region,
    )

    assert selected is None
