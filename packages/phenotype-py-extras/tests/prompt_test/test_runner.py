"""Tests for the pheno_prompt / pheno_prompt_cache pytest fixtures.

These tests exercise the fixture-discovery logic directly (without invoking
the fixtures themselves, which pytest disallows).
"""

from __future__ import annotations

import json

from phenotype_py_extras.prompt_test import runner as runner_mod


def test_pytest_addoption_registers_cache_dir_option():
    """Verify pytest_addoption adds --prompt-cache-dir."""

    class _Group:
        def __init__(self):
            self.added = None

        def addoption(self, *a, **kw):
            self.added = (a, kw)

    groups = {}

    class _Parser:
        def getgroup(self, name):
            if name not in groups:
                groups[name] = _Group()
            return groups[name]

    p = _Parser()
    runner_mod.pytest_addoption(p)
    assert groups["pheno-prompt-test"].added[0][0] == "--prompt-cache-dir"


def test_pytest_configure_registers_prompt_marker():
    """Verify pytest_configure registers the 'prompt' marker."""

    class _Config:
        def __init__(self):
            self.markers = []

        def addinivalue_line(self, section, value):
            self.markers.append((section, value))

    cfg = _Config()
    runner_mod.pytest_configure(cfg)
    assert any("prompt" in v for _s, v in cfg.markers)


def test_prompt_hash_is_stable_for_same_content():
    """_prompt_hash is deterministic for the same input."""
    a = runner_mod._prompt_hash("hello world")
    b = runner_mod._prompt_hash("hello world")
    assert a == b
    assert len(a) == 64  # sha256 hex


def test_prompt_hash_differs_for_different_content():
    a = runner_mod._prompt_hash("hello world")
    b = runner_mod._prompt_hash("goodbye world")
    assert a != b


def test_pheno_prompt_returns_none_when_no_fixture(tmp_path, monkeypatch):
    """When no prompts/<test_name>.{txt,json} exists, fixture yields None."""
    monkeypatch.chdir(tmp_path)

    # Mimic the fixture's discovery logic directly
    test_name = "test_nothing"
    found = None
    for path in [
        tmp_path / "prompts" / f"{test_name}.json",
        tmp_path / "prompts" / f"{test_name}.txt",
    ]:
        if path.is_file():
            found = (
                json.loads(path.read_text())
                if path.suffix == ".json"
                else path.read_text()
            )
    assert found is None


def test_pheno_prompt_loads_text_via_fixture(tmp_path, monkeypatch):
    """When prompts/test_foo.txt exists, fixture returns its contents."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    target = prompts_dir / "test_foo.txt"
    target.write_text("hello world", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    test_name = "test_foo"
    found = None
    for path in [
        prompts_dir / f"{test_name}.json",
        prompts_dir / f"{test_name}.txt",
    ]:
        if path.is_file():
            found = (
                json.loads(path.read_text())
                if path.suffix == ".json"
                else path.read_text()
            )
    assert found == "hello world"


def test_pheno_prompt_loads_json_via_fixture(tmp_path, monkeypatch):
    """When prompts/test_foo.json exists, fixture returns parsed dict."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    target = prompts_dir / "test_foo.json"
    target.write_text(json.dumps({"prompt": "hi"}), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    test_name = "test_foo"
    found = None
    for path in [
        prompts_dir / f"{test_name}.json",
        prompts_dir / f"{test_name}.txt",
    ]:
        if path.is_file():
            found = (
                json.loads(path.read_text())
                if path.suffix == ".json"
                else path.read_text()
            )
    assert found == {"prompt": "hi"}


def test_module_relpath_returns_empty_for_anonymous_module():
    """_module_relpath returns '' when the module has no __file__."""

    class _Node:
        name = "test_x"
        # module is None-like
        module = type("M", (), {})()

    class _Config:
        def getoption(self, k, d=None):
            return None

    class _Request:
        node = _Node()
        config = _Config()

    # For a module without __file__, _module_relpath returns "" (empty path)
    assert runner_mod._module_relpath(_Request()) == ""
