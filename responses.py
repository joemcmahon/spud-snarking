"""YAML response pool loader for Spud bot."""

import random
from pathlib import Path

import yaml


def load_pool(filepath: str) -> list[str]:
    """Load a YAML list from a file. Returns list of strings."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Response pool not found: {filepath}")
    with open(path) as f:
        data = yaml.safe_load(f)
    if data is None:
        return []
    return data


def get_random(pool: list[str]) -> str | None:
    """Return a random item from a pool, or None if empty."""
    if not pool:
        return None
    return random.choice(pool)
