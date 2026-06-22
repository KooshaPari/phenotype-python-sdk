"""Tests for prompt_test assertions (used standalone or via the pytest plugin)."""

from __future__ import annotations

import pytest

from phenotype_py_extras.prompt_test.assertions import (
    assert_prompt_contains,
    assert_prompt_json,
    assert_prompt_match,
)


def test_assert_prompt_match_passes_when_equal():
    assert_prompt_match("hello", "hello")


def test_assert_prompt_match_strips_whitespace_by_default():
    assert_prompt_match("  hello  ", "hello")


def test_assert_prompt_match_fails_on_mismatch():
    with pytest.raises(AssertionError, match="prompt mismatch"):
        assert_prompt_match("hello", "world")


def test_assert_prompt_match_ignore_case():
    assert_prompt_match("HELLO", "hello", ignore_case=True)
    with pytest.raises(AssertionError):
        assert_prompt_match("HELLO", "hello", ignore_case=False)


def test_assert_prompt_match_strip_disabled():
    with pytest.raises(AssertionError):
        assert_prompt_match("  hello  ", "hello", strip=False)


def test_assert_prompt_contains_passes_when_present():
    assert_prompt_contains("the quick brown fox", "brown")


def test_assert_prompt_contains_fails_when_missing():
    with pytest.raises(AssertionError, match="did not contain"):
        assert_prompt_contains("hello", "world")


def test_assert_prompt_contains_as_regex():
    assert_prompt_contains("item-42 here", r"item-\d+", as_regex=True)
    with pytest.raises(AssertionError):
        assert_prompt_contains("item-abc here", r"item-\d+", as_regex=True)


def test_assert_prompt_contains_ignore_case():
    assert_prompt_contains("Hello World", "hello", ignore_case=True)


def test_assert_prompt_json_passes_on_equal_payload():
    assert_prompt_json('{"a": 1, "b": "x"}', {"a": 1, "b": "x"})


def test_assert_prompt_json_fails_on_mismatch():
    with pytest.raises(AssertionError, match="prompt JSON mismatch"):
        assert_prompt_json('{"a": 1}', {"a": 2})


def test_assert_prompt_json_fails_on_invalid_json():
    with pytest.raises(AssertionError, match="not valid JSON"):
        assert_prompt_json("not json", {})