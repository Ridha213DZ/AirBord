from pathlib import Path

import pytest

from app.core.models.profile import Profile
from app.storage.json_profile_repository import (
    JsonProfileRepository,
)


@pytest.fixture
def repository(tmp_path: Path):
    """
    Create an isolated repository for each test.

    pytest provides a temporary directory,
    so tests never modify real application data.
    """

    storage_file = (
        tmp_path / "profiles.json"
    )

    return JsonProfileRepository(
        storage_file=storage_file
    )


def test_repository_creates_storage_file(
    repository,
):
    """
    The storage file should be created
    automatically when the repository is initialized.
    """

    assert repository.storage_file.exists()


def test_save_and_get_profile_by_id(
    repository,
):
    profile = Profile(
        name="Ridha"
    )

    repository.save(
        profile
    )

    loaded = repository.get_by_id(
        profile.id
    )

    assert loaded is not None

    assert loaded.id == profile.id

    assert loaded.name == "Ridha"


def test_get_nonexistent_profile_returns_none(
    repository,
):
    profile = repository.get_by_id(
        "does-not-exist"
    )

    assert profile is None


def test_exists_returns_false_for_unknown_profile(
    repository,
):
    assert repository.exists(
        "does-not-exist"
    ) is False


def test_exists_returns_true_after_save(
    repository,
):
    profile = Profile(
        name="Ridha"
    )

    repository.save(
        profile
    )

    assert repository.exists(
        profile.id
    ) is True


def test_get_all_returns_all_profiles(
    repository,
):
    profile_1 = Profile(
        name="Ridha"
    )

    profile_2 = Profile(
        name="Haytham"
    )

    repository.save(
        profile_1
    )

    repository.save(
        profile_2
    )

    profiles = repository.get_all()

    assert len(
        profiles
    ) == 2

    profile_ids = {
        profile.id
        for profile in profiles
    }

    assert profile_1.id in profile_ids

    assert profile_2.id in profile_ids


def test_get_by_name_returns_matching_profile(
    repository,
):
    profile = Profile(
        name="Ridha"
    )

    repository.save(
        profile
    )

    loaded = repository.get_by_name(
        "Ridha"
    )

    assert loaded is not None

    assert loaded.id == profile.id


def test_get_by_name_returns_none_when_not_found(
    repository,
):
    loaded = repository.get_by_name(
        "Unknown"
    )

    assert loaded is None


def test_save_updates_existing_profile(
    repository,
):
    profile = Profile(
        name="Ridha"
    )

    repository.save(
        profile
    )

    profile.name = (
        "Ridha Berrehouma"
    )

    repository.save(
        profile
    )

    profiles = repository.get_all()

    assert len(
        profiles
    ) == 1

    assert profiles[0].name == (
        "Ridha Berrehouma"
    )


def test_delete_existing_profile(
    repository,
):
    profile = Profile(
        name="Ridha"
    )

    repository.save(
        profile
    )

    deleted = repository.delete(
        profile.id
    )

    assert deleted is True

    assert repository.exists(
        profile.id
    ) is False


def test_delete_unknown_profile_returns_false(
    repository,
):
    deleted = repository.delete(
        "does-not-exist"
    )

    assert deleted is False


def test_get_all_returns_empty_list_when_storage_file_contains_invalid_json(
    tmp_path,
):
    storage_file = tmp_path / "profiles.json"

    storage_file.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    repository = JsonProfileRepository(
        storage_file=storage_file,
    )

    profiles = repository.get_all()

    assert profiles == []


def test_get_all_returns_empty_list_when_storage_file_contains_non_list_json(
    tmp_path,
):
    storage_file = tmp_path / "profiles.json"

    storage_file.write_text(
        '{"profiles": []}',
        encoding="utf-8",
    )

    repository = JsonProfileRepository(
        storage_file=storage_file,
    )

    profiles = repository.get_all()

    assert profiles == []


def test_get_all_returns_empty_list_when_storage_file_contains_non_list_json(
    tmp_path,
):
    storage_file = tmp_path / "profiles.json"

    storage_file.write_text(
        '{"profiles": []}',
        encoding="utf-8",
    )

    repository = JsonProfileRepository(
        storage_file=storage_file,
    )

    profiles = repository.get_all()

    assert profiles == []
