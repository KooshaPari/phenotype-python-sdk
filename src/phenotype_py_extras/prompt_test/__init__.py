"""prompt_test: pytest plugin + assertions for LLM prompt regression testing.

Absorbed from KooshaPari/pheno-prompt-test (L5-114, 2026-06-20).
Public API: pytest plugin (`pheno_prompt_test`) + `assert_prompt_match`/`assert_prompt_contains`
"""

from .runner import pytest_configure, pytest_addoption, pytest_collectstart  # noqa: F401
from .assertions import assert_prompt_match, assert_prompt_contains, assert_prompt_json

__all__ = [
    "assert_prompt_match",
    "assert_prompt_contains",
    "assert_prompt_json",
]