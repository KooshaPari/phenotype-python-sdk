"""Tests for LlmConfig + load_config."""

from __future__ import annotations

from pathlib import Path

import pytest

from phenotype_py_extras.llms_txt.config import LlmConfig, load_config


def test_llmconfig_from_dict_full():
    data = {
        "repo_name": "phenotype-py-extras",
        "tagline": "Python extras",
        "install": "pip install phenotype-py-extras",
        "usage": "from phenotype_py_extras.llms_txt import LlmConfig",
        "public_api": "render, write_llms_txt, init_llms",
        "common_errors": [["ImportError", "pip install phenotype-py-extras"]],
        "references": ["https://llmstxt.org"],
    }
    cfg = LlmConfig.from_dict(data)
    assert cfg.repo_name == "phenotype-py-extras"
    assert cfg.tagline == "Python extras"
    assert cfg.install == "pip install phenotype-py-extras"
    assert cfg.common_errors == [("ImportError", "pip install phenotype-py-extras")]
    assert cfg.references == ["https://llmstxt.org"]


def test_llmconfig_from_dict_defaults():
    cfg = LlmConfig.from_dict({})
    assert cfg.repo_name == ""
    assert cfg.common_errors == []
    assert cfg.references == []


def test_load_config_none_returns_defaults():
    cfg = load_config(None)
    assert cfg.repo_name == ""
    assert cfg.install == ""


def test_load_config_missing_file(tmp_path: Path):
    cfg = load_config(tmp_path / "does_not_exist.yaml")
    assert cfg.repo_name == ""


def test_load_config_round_trip(tmp_path: Path):
    cfg_path = tmp_path / "pheno-llms-txt.yaml"
    cfg_path.write_text(
        "repo_name: demo\n"
        "tagline: hello\n"
        "install: pip install demo\n"
        "usage: import demo\n"
        "public_api: demo.render()\n",
        encoding="utf-8",
    )
    cfg = load_config(cfg_path)
    assert cfg.repo_name == "demo"
    assert cfg.install == "pip install demo"


def test_load_config_top_level_not_mapping(tmp_path: Path):
    cfg_path = tmp_path / "bad.yaml"
    cfg_path.write_text("- one\n- two\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(cfg_path)