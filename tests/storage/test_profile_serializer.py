from datetime import datetime, timezone
from uuid import UUID

import pytest

from app.core.models.face_identity import FaceIdentity
from app.core.models.page import Page
from app.core.models.point import Point
from app.core.models.profile import Profile
from app.core.models.stroke import Stroke


def create_sample_profile() -> Profile:
    """
    Create a realistic profile containing:

        Profile
            ├── FaceIdentity
            └── Pages
                 └── Strokes
                      └── Points

    This gives the serializer a complete
    domain object to convert.
    """

    face_identity = FaceIdentity(
        embedding=[
            0.12,
            0.34,
            0.56,
        ],
        image_path=(
            "data/profiles/"
            "face.jpg"
        ),
    )

    profile = Profile(
        name="Ridha",
        face_identity=face_identity,
    )

    first_page = profile.current_page

    stroke = Stroke(
        color="#FF0000",
        width=8.0,
    )

    stroke.add_point(
        Point(
            x=10.0,
            y=20.0,
        )
    )

    stroke.add_point(
        Point(
            x=30.0,
            y=40.0,
        )
    )

    first_page.add_stroke(
        stroke
    )

    second_page = profile.add_page()

    second_stroke = Stroke(
        color="#0000FF",
        width=3.0,
    )

    second_stroke.add_point(
        Point(
            x=100.0,
            y=200.0,
        )
    )

    second_page.add_stroke(
        second_stroke
    )

    return profile


# ============================================================
# Serialization
# ============================================================


def test_profile_serializer_converts_profile_to_dict():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    assert isinstance(
        data,
        dict,
    )


def test_serialized_profile_contains_required_fields():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    assert data["id"] == str(
        profile.id
    )

    assert data["name"] == (
        profile.name
    )

    assert "face_identity" in data

    assert "pages" in data

    assert "created_at" in data

    assert "updated_at" in data


def test_serialized_profile_is_json_compatible():

    import json

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    serialized = json.dumps(
        data
    )

    assert isinstance(
        serialized,
        str,
    )


# ============================================================
# Deserialization
# ============================================================


def test_profile_serializer_converts_dict_to_profile():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    assert isinstance(
        restored,
        Profile,
    )


def test_deserialized_profile_preserves_identity():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    assert restored.id == (
        profile.id
    )

    assert restored.name == (
        profile.name
    )


def test_deserialized_profile_preserves_face_identity():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    assert (
        restored.face_identity
        is not None
    )

    assert (
        restored.face_identity.id
        ==
        profile.face_identity.id
    )

    assert (
        restored.face_identity.embedding
        ==
        profile.face_identity.embedding
    )

    assert (
        restored.face_identity.image_path
        ==
        profile.face_identity.image_path
    )


# ============================================================
# Pages
# ============================================================


def test_deserialized_profile_preserves_pages():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    assert len(
        restored.pages
    ) == 2

    assert (
        restored.pages[0].id
        ==
        profile.pages[0].id
    )

    assert (
        restored.pages[1].id
        ==
        profile.pages[1].id
    )


# ============================================================
# Strokes
# ============================================================


def test_deserialized_profile_preserves_strokes():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    original_stroke = (
        profile.pages[0].strokes[0]
    )

    restored_stroke = (
        restored.pages[0].strokes[0]
    )

    assert (
        restored_stroke.id
        ==
        original_stroke.id
    )

    assert (
        restored_stroke.color
        ==
        original_stroke.color
    )

    assert (
        restored_stroke.width
        ==
        original_stroke.width
    )


# ============================================================
# Points
# ============================================================


def test_deserialized_profile_preserves_points():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    original_points = (
        profile.pages[0]
        .strokes[0]
        .points
    )

    restored_points = (
        restored.pages[0]
        .strokes[0]
        .points
    )

    assert len(
        restored_points
    ) == len(
        original_points
    )

    for original, restored_point in zip(
        original_points,
        restored_points,
    ):

        assert (
            restored_point.x
            ==
            original.x
        )

        assert (
            restored_point.y
            ==
            original.y
        )


# ============================================================
# Dates
# ============================================================


def test_deserialized_profile_preserves_dates():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = create_sample_profile()

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    assert (
        restored.created_at
        ==
        profile.created_at
    )

    assert (
        restored.updated_at
        ==
        profile.updated_at
    )


# ============================================================
# Optional FaceIdentity
# ============================================================


def test_profile_without_face_identity_round_trips():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    profile = Profile(
        name="New User"
    )

    data = ProfileSerializer.to_dict(
        profile
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    assert (
        restored.face_identity
        is None
    )

    assert (
        restored.name
        ==
        "New User"
    )


# ============================================================
# Complete round trip
# ============================================================


def test_complete_profile_round_trip():

    from app.storage.serializers.profile_serializer import (
        ProfileSerializer,
    )

    original = create_sample_profile()

    data = ProfileSerializer.to_dict(
        original
    )

    restored = ProfileSerializer.from_dict(
        data
    )

    assert (
        restored.id
        ==
        original.id
    )

    assert (
        restored.name
        ==
        original.name
    )

    assert len(
        restored.pages
    ) == len(
        original.pages
    )

    assert (
        restored.face_identity.embedding
        ==
        original.face_identity.embedding
    )