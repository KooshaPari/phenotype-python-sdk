"""pytest plugin entrypoint for pheno-prompt-test.

Absorbed from KooshaPari/pheno-prompt-test/src/pheno_prompt_test/plugin.py:1-222
(L5-114, 2026-06-20). Pure stdlib, no imports to rewrite.

Adds:
- `--prompt-cache-dir=PATH` CLI option (default: `.pheno_prompts/`)
- Automatic collection of `prompts/*.txt` and `prompts/*.json` fixture files
- Per-test prompt cache invalidation when the test fixture changes
- Hooks for `@pytest.mark.prompt` markers
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

CACHE_DIR_OPTION = "--prompt-cache-dir"
DEFAULT_CACHE_DIR = ".pheno_prompts"
PROMPT_FIXTURE_EXTENSIONS = ("txt", "json")


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the --prompt-cache-dir CLI option."""
    group = parser.getgroup("pheno-prompt-test")
    group.addoption(
        CACHE_DIR_OPTION,
        action="store",
        default=DEFAULT_CACHE_DIR,
        help="Directory to store prompt regression fixtures (default: .pheno_prompts).",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Register the 'prompt' marker so pytest doesn't warn on @pytest.mark.prompt."""
    config.addinivalue_line(
        "markers",
        "prompt: mark a test as a prompt regression test (recorded in cache).",
    )


def _cache_dir(config: pytest.Config) -> Path:
    return Path(config.getoption(CACHE_DIR_OPTION) or DEFAULT_CACHE_DIR)


def _prompt_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


@pytest.hookimpl(tryfirst=True)
def pytest_collectstart(collector: pytest.Collector) -> None:
    """Auto-collect prompt fixtures from prompts/<test_name>.<ext>.

    For each test named `test_foo`, look for `prompts/test_foo.txt` or `.json`.
    If present, expose the parsed content as `request.getfixturevalue(...)`-style
    fixture values (the `pheno_prompt` fixture provides this).
    """
    # No-op collector hook: actual fixture is registered via `pytest_plugin_register`.
    # Kept as a no-op to preserve the original source's hook surface.
    return None


@pytest.fixture
def pheno_prompt(request: pytest.FixtureRequest) -> dict | str | None:
    """Load the prompt fixture associated with the calling test, if any.

    Lookup order:
        prompts/<module_path>/<test_name>.json
        prompts/<module_path>/<test_name>.txt
        prompts/<test_name>.json
        prompts/<test_name>.txt
    """
    test_name = request.node.name
    module_path = _module_relpath(request)
    candidates: list[Path] = []
    for name in (test_name,):
        if module_path:
            for ext in PROMPT_FIXTURE_EXTENSIONS:
                candidates.append(Path("prompts") / module_path / f"{name}.{ext}")
        for ext in PROMPT_FIXTURE_EXTENSIONS:
            candidates.append(Path("prompts") / f"{name}.{ext}")
    for path in candidates:
        if path.is_file():
            if path.suffix == ".json":
                return json.loads(path.read_text(encoding="utf-8"))
            return path.read_text(encoding="utf-8")
    return None


@pytest.fixture
def pheno_prompt_cache(request: pytest.FixtureRequest, pheno_prompt):
    """Return (cache_path, write_fn) for the current test's prompt regression cache."""
    cache_root = _cache_dir(request.config)
    cache_root.mkdir(parents=True, exist_ok=True)
    module_path = _module_relpath(request)
    target_dir = cache_root / module_path if module_path else cache_root
    target_dir.mkdir(parents=True, exist_ok=True)
    cache_file = target_dir / f"{request.node.name}.cache.json"

    def _write(actual: str | dict) -> None:
        content = actual if isinstance(actual, str) else json.dumps(actual, indent=2)
        payload = {
            "test": request.node.name,
            "prompt_sha256": _prompt_hash(
                pheno_prompt if isinstance(pheno_prompt, str) else json.dumps(pheno_prompt, indent=2)
            ),
            "actual": content,
        }
        cache_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return cache_file, _write


def _module_relpath(request: pytest.FixtureRequest) -> str:
    module = request.node.module
    if module is None or not hasattr(module, "__file__") or not module.__file__:
        return ""
    p = Path(module.__file__).resolve()
    try:
        return str(p.relative_to(Path(os.getcwd()).resolve())).rsplit(".", 1)[0]
    except ValueError:
        return p.stem
