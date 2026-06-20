"""Validation helpers for LlmConfig.

Absorbed from KooshaPari/pheno-llms-txt (V6 PR-3 init_llms scaffold-kit) (L5-114, 2026-06-20).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .config import LlmConfig, load_config
from .renderer import write_llms_txt


class ConfigError(ValueError):
    """Raised when an LlmConfig fails validation."""


def validate_config(cfg: LlmConfig) -> None:
    """Raise ConfigError if cfg is missing required fields. Idempotent + side-effect-free."""
    if not cfg.repo_name.strip():
        raise ConfigError("repo_name is required")
    if not cfg.tagline.strip():
        raise ConfigError("tagline is required")
    if not cfg.install.strip():
        raise ConfigError("install section is required")
    if not cfg.usage.strip():
        raise ConfigError("usage section is required")
    for i, (title, _fix) in enumerate(cfg.common_errors):
        if not title.strip():
            raise ConfigError(f"common_errors[{i}].title is empty")


_STARTER_YAML = """\
repo_name: {repo_name}
tagline: {tagline}
install: |
  pip install {repo_name}
usage: |
  from {module_name} import ...
public_api: |
  # TBD
common_errors: []
references: []
"""


def init_llms(
    repo_dir: str | Path,
    *,
    repo_name: str = "my-project",
    tagline: str = "Short one-line description.",
    module_name: Optional[str] = None,
    config_filename: str = "pheno-llms-txt.yaml",
    llms_filename: str = "llms.txt",
) -> dict:
    """V6 PR-3 scaffold-kit entrypoint: write a starter YAML (idempotent) + render llms.txt.

    Returns a structured dict for orchestrator use:
        {"config_path": ..., "llms_path": ..., "created_config": bool}
    """
    repo = Path(repo_dir)
    repo.mkdir(parents=True, exist_ok=True)
    config_path = repo / config_filename
    llms_path = repo / llms_filename

    created_config = False
    if not config_path.exists():
        module_name = module_name or repo_name.replace("-", "_")
        config_path.write_text(
            _STARTER_YAML.format(repo_name=repo_name, tagline=tagline, module_name=module_name),
            encoding="utf-8",
        )
        created_config = True

    cfg = load_config(config_path)
    validate_config(cfg)
    written = write_llms_txt(cfg, llms_path)
    return {
        "config_path": str(config_path),
        "llms_path": str(written),
        "created_config": created_config,
    }