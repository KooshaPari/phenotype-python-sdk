"""Pytest configuration for ResilienceKit tests.

This conftest isolates ResilienceKit tests from the root conftest.py
to avoid dependency issues with pytest-asyncio and SQLAlchemy.
"""

import sys
from pathlib import Path

# Calculate absolute paths from this file's location
_RESILIENCE_KIT_ROOT = Path(__file__).parent.parent.resolve()
_REPOS_ROOT = _RESILIENCE_KIT_ROOT.parent

# Add Python package source directories (absolute paths)
_package_paths = [
    _RESILIENCE_KIT_ROOT / "python" / "deploy-kit" / "src",
    _RESILIENCE_KIT_ROOT / "python" / "pheno-resilience" / "src",
    _REPOS_ROOT / "pheno" / "python" / "pheno-core" / "src",
]

for src_path in _package_paths:
    if src_path.exists():
        src_path_str = str(src_path)
        if src_path_str not in sys.path:
            sys.path.insert(0, src_path_str)
