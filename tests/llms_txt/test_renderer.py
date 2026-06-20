"""Tests for render() + write_llms_txt()."""

from __future__ import annotations

from pathlib import Path

from phenotype_py_extras.llms_txt.config import LlmConfig
from phenotype_py_extras.llms_txt.renderer import render, write_llms_txt


def _full_cfg() -> LlmConfig:
    return LlmConfig(
        repo_name="phenotype-py-extras",
        tagline="Consolidated Python extras.",
        install="pip install phenotype-py-extras",
        usage="from phenotype_py_extras.llms_txt import LlmConfig",
        public_api="render, write_llms_txt, init_llms, cli_main",
        common_errors=[("ImportError", "pip install phenotype-py-extras")],
        references=["https://llmstxt.org"],
    )


def test_render_includes_repo_name_and_tagline():
    out = render(_full_cfg())
    assert "# phenotype-py-extras" in out
    assert "Consolidated Python extras." in out


def test_render_includes_install_usage_public_api():
    out = render(_full_cfg())
    assert "## Install" in out
    assert "## Usage" in out
    assert "## Public API" in out
    assert "pip install phenotype-py-extras" in out


def test_render_includes_common_errors_block():
    out = render(_full_cfg())
    assert "## Common errors" in out
    assert "**ImportError**" in out


def test_render_includes_references_block():
    out = render(_full_cfg())
    assert "## See also" in out
    assert "https://llmstxt.org" in out


def test_render_minimal_cfg_omits_optional_blocks():
    cfg = LlmConfig(repo_name="r", tagline="t", install="i", usage="u", public_api="p")
    out = render(cfg)
    assert "# r" in out
    assert "## Common errors" not in out
    assert "## See also" not in out


def test_write_llms_txt_writes_to_disk(tmp_path: Path):
    target = tmp_path / "out.txt"
    p = write_llms_txt(_full_cfg(), target)
    assert p == target
    assert target.exists()
    content = target.read_text(encoding="utf-8")
    assert "phenotype-py-extras" in content


def test_write_llms_txt_default_filename(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    p = write_llms_txt(_full_cfg())
    assert p.name == "llms.txt"
    assert p.exists()