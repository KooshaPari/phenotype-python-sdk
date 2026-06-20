"""render() + write_llms_txt() + TEMPLATE constant.

Absorbed from KooshaPari/pheno-llms-txt/src/pheno_llms_txt/core.py:24-96 (L5-114, 2026-06-20).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .config import LlmConfig


TEMPLATE = """# {repo_name}

> {tagline}

## Install

{install}

## Usage

{usage}

## Public API

{public_api}
{common_errors_block}
{references_block}
"""


def _format_common_errors(errors: list[tuple[str, str]]) -> str:
    if not errors:
        return ""
    lines = ["\n## Common errors\n"]
    for title, fix in errors:
        lines.append(f"- **{title}** — {fix}")
    return "\n".join(lines) + "\n"


def _format_references(refs: list[str]) -> str:
    if not refs:
        return ""
    lines = ["\n## See also\n"]
    for ref in refs:
        lines.append(f"- {ref}")
    return "\n".join(lines) + "\n"


def render(cfg: LlmConfig) -> str:
    """Render an llms.txt string from a populated LlmConfig."""
    return TEMPLATE.format(
        repo_name=cfg.repo_name,
        tagline=cfg.tagline,
        install=cfg.install,
        usage=cfg.usage,
        public_api=cfg.public_api,
        common_errors_block=_format_common_errors(cfg.common_errors),
        references_block=_format_references(cfg.references),
    )


def write_llms_txt(cfg: LlmConfig, out_path: Optional[str | Path] = "llms.txt") -> Path:
    """Render and write to disk. Returns the Path written."""
    p = Path(out_path or "llms.txt")
    p.write_text(render(cfg), encoding="utf-8")
    return p