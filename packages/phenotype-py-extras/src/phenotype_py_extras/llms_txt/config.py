"""LlmConfig dataclass + load_config (yaml-driven).

Absorbed from KooshaPari/pheno-llms-txt/src/pheno_llms_txt/core.py:1-96 (L5-114, 2026-06-20).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class LlmConfig:
    """Configuration for an llms.txt render."""

    repo_name: str
    tagline: str
    install: str
    usage: str
    public_api: str
    common_errors: list[tuple[str, str]] = field(default_factory=list)
    references: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "LlmConfig":
        """Build LlmConfig from a parsed YAML dict.

        Tolerates missing keys; defaults are empty strings / lists.
        """
        errors_raw = data.get("common_errors", []) or []
        errors = [tuple(e) for e in errors_raw] if errors_raw else []
        return cls(
            repo_name=str(data.get("repo_name", "")),
            tagline=str(data.get("tagline", "")),
            install=str(data.get("install", "")),
            usage=str(data.get("usage", "")),
            public_api=str(data.get("public_api", "")),
            common_errors=errors,
            references=list(data.get("references", []) or []),
        )


def load_config(path: Optional[str | Path]) -> LlmConfig:
    """Load LlmConfig from a YAML file. Returns defaults if path is None/missing."""
    if path is None:
        return LlmConfig(
            repo_name="",
            tagline="",
            install="",
            usage="",
            public_api="",
        )
    p = Path(path)
    if not p.exists():
        return LlmConfig(
            repo_name="",
            tagline="",
            install="",
            usage="",
            public_api="",
        )
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML must be a mapping, got {type(data).__name__}")
    return LlmConfig.from_dict(data)