import inspect

from app.storage.repositories.profile_repository import (
    ProfileRepository,
)


def test_profile_repository_is_abstract():

    assert inspect.isabstract(
        ProfileRepository
    )


def test_profile_repository_defines_save():

    assert hasattr(
        ProfileRepository,
        "save",
    )


def test_profile_repository_defines_get_by_id():

    assert hasattr(
        ProfileRepository,
        "get_by_id",
    )


def test_profile_repository_defines_get_by_name():

    assert hasattr(
        ProfileRepository,
        "get_by_name",
    )


def test_profile_repository_defines_get_all():

    assert hasattr(
        ProfileRepository,
        "get_all",
    )


def test_profile_repository_defines_delete():

    assert hasattr(
        ProfileRepository,
        "delete",
    )


def test_profile_repository_defines_exists():

    assert hasattr(
        ProfileRepository,
        "exists",
    )