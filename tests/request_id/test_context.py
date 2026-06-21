"""Tests for request_id context (set/get/reset/new)."""

from __future__ import annotations

from phenotype_py_extras.request_id.context import (
    clear_request_id,
    get_request_id,
    new_request_id,
    request_id_var,
    reset_request_id,
    set_request_id,
)


def test_default_request_id_is_none():
    assert get_request_id() is None


def test_set_and_get_roundtrip():
    token = set_request_id("abc123")
    try:
        assert get_request_id() == "abc123"
    finally:
        reset_request_id(token)
    assert get_request_id() is None


def test_new_request_id_returns_hex_string():
    rid = new_request_id()
    assert isinstance(rid, str)
    assert len(rid) == 32
    int(rid, 16)


def test_new_request_id_uniqueness():
    a, b = new_request_id(), new_request_id()
    assert a != b


def test_clear_request_id_unsets_value():
    set_request_id("xyz")
    clear_request_id()
    assert get_request_id() is None


def test_request_id_var_is_contextvars_instance():
    import contextvars

    assert isinstance(request_id_var, contextvars.ContextVar)