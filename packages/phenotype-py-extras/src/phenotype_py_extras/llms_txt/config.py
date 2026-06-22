"""LlmConfig dataclass + load_config (yaml-driven).

Absorbed from KooshaPari/pheno-llms-txt/src/pheno_llms_txt/core.py:1-96 (L5-114, 2026-06-20).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Any

import yaml


class ConfigError(ValueError):
    """Raised when an LlmConfig cannot be built from user configuration."""


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
        return cls(
            repo_name=str(data.get("repo_name", "")),
            tagline=str(data.get("tagline", "")),
            install=str(data.get("install", "")),
            usage=str(data.get("usage", "")),
            public_api=str(data.get("public_api", "")),
            common_errors=_coerce_common_errors(data.get("common_errors", [])),
            references=_coerce_string_list(data.get("references", []), "references"),
        )


def _coerce_common_errors(value: Any) -> list[tuple[str, str]]:
    if value is None:
        return []
    if isinstance(value, (str, bytes)) or not isinstance(value, list):
        raise ConfigError("common_errors must be a list of [title, fix] pairs")
    errors: list[tuple[str, str]] = []
    for index, item in enumerate(value):
        if (
            isinstance(item, (str, bytes))
            or not isinstance(item, (list, tuple))
            or len(item) != 2
        ):
            raise ConfigError(f"common_errors[{index}] must be a [title, fix] pair")
        title, fix = item
        errors.append((str(title), str(fix)))
    return errors


def _coerce_string_list(value: Any, field_name: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, bytes) or not isinstance(value, list):
        raise ConfigError(f"{field_name} must be a string or list of strings")
    return [str(item) for item in value]


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
        raise ConfigError(f"Top-level YAML must be a mapping, got {type(data).__name__}")
    return LlmConfig.from_dict(data)
