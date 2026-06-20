"""Tests for validate_config() + init_llms()."""

from __future__ import annotations

from pathlib import Path

import pytest

from phenotype_py_extras.llms_txt.config import LlmConfig
from phenotype_py_extras.llms_txt.validator import (
    ConfigError,
    init_llms,
    validate_config,
)


def _valid_cfg() -> LlmConfig:
    return LlmConfig(
        repo_name="r",
        tagline="t",
        install="i",
        usage="u",
        public_api="p",
        common_errors=[("E", "F")],
    )


def test_validate_config_passes_for_full_cfg():
    validate_config(_valid_cfg())


def test_validate_config_missing_repo_name_raises():
    cfg = _valid_cfg()
    cfg.repo_name = ""
    with pytest.raises(ConfigError, match="repo_name"):
        validate_config(cfg)


def test_validate_config_missing_tagline_raises():
    cfg = _valid_cfg()
    cfg.tagline = ""
    with pytest.raises(ConfigError, match="tagline"):
        validate_config(cfg)


def test_validate_config_missing_install_raises():
    cfg = _valid_cfg()
    cfg.install = ""
    with pytest.raises(ConfigError, match="install"):
        validate_config(cfg)


def test_validate_config_missing_usage_raises():
    cfg = _valid_cfg()
    cfg.usage = ""
    with pytest.raises(ConfigError, match="usage"):
        validate_config(cfg)


def test_validate_config_empty_common_error_title_raises():
    cfg = _valid_cfg()
    cfg.common_errors = [("", "fix")]
    with pytest.raises(ConfigError, match="common_errors"):
        validate_config(cfg)


def test_init_llms_creates_starter_files(tmp_path: Path):
    out = init_llms(tmp_path, repo_name="demo", tagline="hello")
    cfg_path = tmp_path / "pheno-llms-txt.yaml"
    llms_path = tmp_path / "llms.txt"
    assert cfg_path.exists()
    assert llms_path.exists()
    assert out["created_config"] is True
    assert out["config_path"] == str(cfg_path)
    assert out["llms_path"] == str(llms_path)


def test_init_llms_is_idempotent(tmp_path: Path):
    init_llms(tmp_path, repo_name="demo", tagline="hello")
    out = init_llms(tmp_path, repo_name="demo", tagline="hello")
    assert out["created_config"] is False


def test_init_llms_renders_repo_name_into_output(tmp_path: Path):
    init_llms(tmp_path, repo_name="my-thing", tagline="my tagline")
    content = (tmp_path / "llms.txt").read_text(encoding="utf-8")
    assert "my-thing" in content
    assert "my tagline" in content