"""Pytest configuration and shared fixtures for PhenoKits tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Root directory of the PhenoKits repository
REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture
def repo_root() -> Path:
    """Return the root directory of the PhenoKits repository."""
    return REPO_ROOT


@pytest.fixture
def category_dirs(repo_root: Path) -> dict[str, Path]:
    """Return paths to all 12 category directories."""
    categories = [
        "templates",
        "configs",
        "libs",
        "secrets",
        "governance",
        "security",
        "observability",
        "docs",
        "scripts",
        "schemas",
        "policies",
        "credentials",
    ]
    return {name: repo_root / name for name in categories}


@pytest.fixture
def python_libs_dir(repo_root: Path) -> Path:
    """Return the path to the Python libraries directory."""
    return repo_root / "libs" / "python"


@pytest.fixture
def hexakit_dir(repo_root: Path) -> Path:
    """Return the path to the HexaKit submodule."""
    return repo_root / "HexaKit"
