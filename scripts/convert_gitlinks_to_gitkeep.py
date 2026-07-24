"""Convert malformed nested gitlinks to regular directory placeholders.

Background
----------

The rationalization absorb (commit ``f5f4e75``) registered 8 nested
``mode 160000`` entries for sub-packages that no longer have reachable
commits in the consolidated object database. Replacing them with a
tracked ``.gitkeep`` file preserves the path layout (so external
downstreams that depend on the directory's existence continue to work)
without leaving the index poisoned by dangling gitlinks.

Each conversion is one ``git rm --cached`` + ``git add`` of a single
``.gitkeep`` file.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GITLINKS = [
    "packages/auth-kit/go",
    "packages/auth-kit/python/pheno-auth",
    "packages/auth-kit/python/pheno-security",
    "packages/observability-kit/python/pheno-logging",
    "packages/observability-kit/python/pheno-observability",
    "packages/observability-kit/rust/helix-logging",
    "packages/observability-kit/rust/helix-tracing",
    "packages/testing-kit/python/pheno-quality",
]


def _run(*args: str) -> None:
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def main() -> int:
    for rel in GITLINKS:
        target = REPO_ROOT / rel
        target.mkdir(parents=True, exist_ok=True)
        keep = target / ".gitkeep"
        keep.touch(exist_ok=True)

        _run("git", "rm", "--cached", "--ignore-unmatch", rel)
        _run("git", "add", str(keep.relative_to(REPO_ROOT)))
        print(f"converted {rel} -> {keep.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
