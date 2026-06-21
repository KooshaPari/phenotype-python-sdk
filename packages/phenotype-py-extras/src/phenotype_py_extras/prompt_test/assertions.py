"""Assertion helpers for prompt regression tests.

Absorbed (semantically) from KooshaPari/pheno-prompt-test/src/pheno_prompt_test/plugin.py
(L5-114, 2026-06-20). The original source kept these inline in `plugin.py`; here
they are split out for direct import without requiring the pytest plugin to be loaded.

Use either via the `pheno_prompt_test` pytest plugin (auto-loaded), or as plain
helpers in non-pytest code:
    from phenotype_py_extras.prompt_test import assert_prompt_match
    assert_prompt_match(actual, expected, *, strip=True, ignore_case=False)
"""

from __future__ import annotations

import json
import re
from typing import Any


def _normalize(s: str, strip: bool, ignore_case: bool) -> str:
    out = s.strip() if strip else s
    out = out.lower() if ignore_case else out
    return out


def assert_prompt_match(
    actual: str,
    expected: str,
    *,
    strip: bool = True,
    ignore_case: bool = False,
) -> None:
    """Assert `actual` equals `expected` after normalization."""
    a = _normalize(actual, strip, ignore_case)
    e = _normalize(expected, strip, ignore_case)
    if a != e:
        raise AssertionError(
            f"prompt mismatch:\n  expected: {e!r}\n  actual:   {a!r}"
        )


def assert_prompt_contains(
    actual: str,
    needle: str,
    *,
    ignore_case: bool = False,
    as_regex: bool = False,
) -> None:
    """Assert `actual` contains `needle` (substring or regex match)."""
    a = actual.lower() if ignore_case else actual
    n = needle.lower() if ignore_case else needle
    if as_regex:
        if not re.search(n, a):
            raise AssertionError(f"prompt did not match regex {needle!r}; got: {actual!r}")
        return
    if n not in a:
        raise AssertionError(f"prompt did not contain {needle!r}; got: {actual!r}")


def assert_prompt_json(actual: str, expected: Any, *, ignore_case_keys: bool = False) -> None:
    """Assert `actual` parses as JSON equal to `expected`."""
    try:
        parsed = json.loads(actual)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"prompt is not valid JSON: {exc}; got: {actual!r}") from exc
    if ignore_case_keys:
        parsed = {k.lower(): v for k, v in parsed.items()} if isinstance(parsed, dict) else parsed
    if parsed != expected:
        raise AssertionError(
            f"prompt JSON mismatch:\n  expected: {expected!r}\n  actual:   {parsed!r}"
        )