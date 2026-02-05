import os
import pytest
from responses import load_pool, get_random


@pytest.fixture
def sample_yaml(tmp_path):
    """Create a temporary YAML file with test data."""
    p = tmp_path / "test_pool.yml"
    p.write_text('- "alpha"\n- "bravo"\n- "charlie"\n')
    return str(p)


@pytest.fixture
def empty_yaml(tmp_path):
    """Create an empty YAML file."""
    p = tmp_path / "empty.yml"
    p.write_text("---\n")
    return str(p)


def test_load_pool_returns_list(sample_yaml):
    pool = load_pool(sample_yaml)
    assert pool == ["alpha", "bravo", "charlie"]


def test_load_pool_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_pool("/nonexistent/path.yml")


def test_load_pool_empty_file_returns_empty_list(empty_yaml):
    pool = load_pool(empty_yaml)
    assert pool == []


def test_get_random_returns_item_from_pool():
    pool = ["alpha", "bravo", "charlie"]
    result = get_random(pool)
    assert result in pool


def test_get_random_empty_pool_returns_none():
    result = get_random([])
    assert result is None
