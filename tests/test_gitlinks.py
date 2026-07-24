"""Regression tests for malformed nested gitlinks in this monorepo.

Background
----------

The rationalization commit ``f5f4e75 feat: absorb AuthKit/DataKit/McpKit/
ObservabilityKit/ResilienceKit/TestingKit/PhenoKits into python SDK
monorepo`` introduced nested ``mode 160000`` (gitlink) entries for paths
that were never registered in ``.gitmodules`` and whose target commits
are no longer reachable in the consolidated object database. The
manifestation is:

    fatal: no submodule mapping found in .gitmodules for path
    'packages/auth-kit/go'

Any ``uv``-backed downstream that calls ``git submodule status`` while
resolving dependencies fails immediately, which blocks consumers such
as ``thegent`` (``task test``).

These tests pin the desired end-state: every ``mode 160000`` entry in
the index must either be (a) absent entirely, or (b) accompanied by a
matching ``.gitmodules`` entry whose target commit is present in the
local object database.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GITMODULES = REPO_ROOT / ".gitmodules"


def _run_git(*args: str) -> str:
    result = subprocess.run(
        ("git",) + args,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout + result.stderr


def _index_gitlinks() -> list[tuple[str, str]]:
    """Return (path, sha) tuples for every index entry in mode 160000."""

    out = subprocess.run(
        ("git", "ls-files", "--stage"),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    gitlinks: list[tuple[str, str]] = []
    for line in out.splitlines():
        parts = line.split("\t", 1)
        if not parts:
            continue
        meta, path = parts[0], parts[1]
        mode, sha, *_ = meta.split()
        if mode == "160000":
            gitlinks.append((path, sha))
    return gitlinks


def _parse_gitmodules(text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for block in re.split(r"\n(?=\[submodule )", text):
        name_match = re.search(r'\[submodule "([^"]+)"\]', block)
        if not name_match:
            continue
        name = name_match.group(1)
        path_match = re.search(r"path\s*=\s*(.+)", block)
        if path_match:
            mapping[name] = path_match.group(1).strip()
    return mapping


def _has_object(sha: str) -> bool:
    if not sha:
        return False
    proc = subprocess.run(
        ("git", "cat-file", "-e", sha),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


# --- Required: no malformed gitlinks remain ------------------------------


def test_no_unregistered_gitlinks() -> None:
    """Every gitlink in the index is registered in ``.gitmodules``."""

    gitlinks = _index_gitlinks()

    raw = GITMODULES.read_text() if GITMODULES.exists() else ""
    submodules_by_name = _parse_gitmodules(raw)
    submodules_by_path = {v: k for k, v in submodules_by_name.items()}

    unregistered: list[str] = []
    unreachable: list[tuple[str, str]] = []
    for path, sha in gitlinks:
        if path not in submodules_by_path.values():
            unregistered.append(f"{path} ({sha})")
            continue
        if not _has_object(sha):
            unreachable.append((path, sha))

    problems: list[str] = []
    if unregistered:
        problems.append(
            "gitlinks with no .gitmodules entry: " + ", ".join(unregistered)
        )
    if unreachable:
        problems.append(
            "gitlinks whose target commit is missing: "
            + ", ".join(f"{p} ({s})" for p, s in unreachable)
        )

    assert not problems, problems[0] if len(problems) == 1 else problems


def test_git_submodule_status_does_not_error() -> None:
    """``git submodule status --recursive`` reports no fatal errors."""

    out = _run_git("submodule", "status", "--recursive")
    assert "fatal" not in out, (
        "git submodule status --recursive produced a fatal error:\n" + out
    )


def test_no_url_found_for_submodule_path() -> None:
    """``git submodule update --init --recursive`` does not emit the
    ``No url found for submodule path`` error."""

    out = _run_git("submodule", "update", "--init", "--recursive", "--dry-run")
    assert "No url found for submodule path" not in out, out
    assert "fatal: no submodule mapping found in .gitmodules" not in out, out
