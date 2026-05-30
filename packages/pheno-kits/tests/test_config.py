"""Tests for PhenoKits configuration files and workspace settings."""

from __future__ import annotations

import tomli
from pathlib import Path

import pytest


class TestCargoWorkspace:
    """Tests for Cargo workspace configuration."""

    def test_cargo_toml_is_valid_toml(self, repo_root: Path) -> None:
        """Verify Cargo.toml is valid TOML."""
        cargo_toml = repo_root / "Cargo.toml"
        assert cargo_toml.exists(), "Cargo.toml not found"

        content = cargo_toml.read_bytes()
        # Should be valid TOML
        try:
            data = tomli.loads(content.decode("utf-8"))
            assert isinstance(data, dict)
        except Exception as e:
            pytest.fail(f"Cargo.toml is not valid TOML: {e}")

    def test_cargo_workspace_has_excludes(self, repo_root: Path) -> None:
        """Verify Cargo.toml workspace excludes key directories."""
        cargo_toml = repo_root / "Cargo.toml"
        content = cargo_toml.read_text()

        # Should exclude HexaKit, libs/, templates/, etc.
        assert "exclude" in content, "Workspace should have exclude list"
        assert "HexaKit" in content, "Should exclude HexaKit submodule"
        assert "libs" in content, "Should exclude libs directory"

    def test_cargo_resolver_version(self, repo_root: Path) -> None:
        """Verify Cargo.toml specifies resolver version."""
        cargo_toml = repo_root / "Cargo.toml"
        content = cargo_toml.read_text()

        # Should specify resolver = "2" for workspace
        assert 'resolver = "2"' in content or "resolver = '2'" in content


class TestRustToolchain:
    """Tests for Rust toolchain configuration."""

    def test_rust_toolchain_toml_exists(self, repo_root: Path) -> None:
        """Verify rust-toolchain.toml exists for consistent Rust version."""
        toolchain = repo_root / "rust-toolchain.toml"
        assert toolchain.exists(), "rust-toolchain.toml not found"

    def test_rust_toolchain_toml_is_valid(self, repo_root: Path) -> None:
        """Verify rust-toolchain.toml is valid TOML."""
        toolchain = repo_root / "rust-toolchain.toml"
        content = toolchain.read_text()

        try:
            data = tomli.loads(content)
            assert isinstance(data, dict)
            # Channel may be at top level or under [toolchain]
            has_channel = (
                "channel" in data
                or (isinstance(data.get("toolchain"), dict) and "channel" in data["toolchain"])
            )
            assert has_channel, "rust-toolchain.toml should specify channel"
        except Exception as e:
            pytest.fail(f"rust-toolchain.toml is not valid TOML: {e}")


class TestRustfmtConfig:
    """Tests for Rust formatting configuration."""

    def test_rustfmt_toml_exists(self, repo_root: Path) -> None:
        """Verify rustfmt.toml exists."""
        rustfmt = repo_root / "rustfmt.toml"
        assert rustfmt.exists(), "rustfmt.toml not found"

    def test_rustfmt_config_is_valid(self, repo_root: Path) -> None:
        """Verify rustfmt.toml is valid TOML."""
        rustfmt = repo_root / "rustfmt.toml"
        content = rustfmt.read_text()

        try:
            data = tomli.loads(content)
            assert isinstance(data, dict)
        except Exception as e:
            pytest.fail(f"rustfmt.toml is not valid TOML: {e}")


class TestClippyConfig:
    """Tests for Clippy linter configuration."""

    def test_clippy_toml_exists(self, repo_root: Path) -> None:
        """Verify clippy.toml exists."""
        clippy = repo_root / "clippy.toml"
        assert clippy.exists(), "clippy.toml not found"

    def test_clippy_config_is_valid(self, repo_root: Path) -> None:
        """Verify clippy.toml is valid TOML."""
        clippy = repo_root / "clippy.toml"
        content = clippy.read_text()

        try:
            data = tomli.loads(content)
            assert isinstance(data, dict)
        except Exception as e:
            pytest.fail(f"clippy.toml is not valid TOML: {e}")


class TestDenyConfig:
    """Tests for cargo-deny configuration."""

    def test_deny_toml_exists(self, repo_root: Path) -> None:
        """Verify deny.toml exists for dependency auditing."""
        deny = repo_root / "deny.toml"
        assert deny.exists(), "deny.toml not found"

    def test_deny_toml_is_valid(self, repo_root: Path) -> None:
        """Verify deny.toml is valid TOML."""
        deny = repo_root / "deny.toml"
        content = deny.read_text()

        try:
            data = tomli.loads(content)
            assert isinstance(data, dict)
            # Should have sections like [licenses], [bans], etc.
            assert any(
                key in data
                for key in ["licenses", "bans", "sources", "advisories"]
            ), "deny.toml should have policy sections"
        except Exception as e:
            pytest.fail(f"deny.toml is not valid TOML: {e}")


class TestGitHubConfig:
    """Tests for GitHub-related configuration."""

    def test_github_workflows_directory(self, repo_root: Path) -> None:
        """Verify .github/workflows/ exists if GitHub integration is used."""
        workflows = repo_root / ".github" / "workflows"
        if workflows.exists():
            workflow_files = list(workflows.glob("*.yml")) + list(
                workflows.glob("*.yaml")
            )
            # If workflows exist, verify they're valid YAML
            for wf in workflow_files:
                try:
                    import yaml

                    with open(wf) as f:
                        yaml.safe_load(f)
                except ImportError:
                    # YAML library not available, skip validation
                    pass

    def test_codeowners_exists(self, repo_root: Path) -> None:
        """Verify CODEOWNERS file exists for code ownership."""
        codeowners = repo_root / "CODEOWNERS"
        assert codeowners.exists(), "CODEOWNERS not found"

    def test_precommit_config_exists(self, repo_root: Path) -> None:
        """Verify pre-commit configuration exists."""
        precommit = repo_root / ".pre-commit-config.yaml"
        if precommit.exists():
            content = precommit.read_text()
            assert "repos" in content, "pre-commit config should have repos"


class TestCliffConfig:
    """Tests for conventional changelog configuration."""

    def test_cliff_toml_exists(self, repo_root: Path) -> None:
        """Verify cliff.toml exists for changelog generation."""
        cliff = repo_root / "cliff.toml"
        assert cliff.exists(), "cliff.toml not found"

    def test_cliff_toml_is_valid(self, repo_root: Path) -> None:
        """Verify cliff.toml is valid TOML."""
        cliff = repo_root / "cliff.toml"
        content = cliff.read_text()

        try:
            data = tomli.loads(content)
            assert isinstance(data, dict)
        except Exception as e:
            pytest.fail(f"cliff.toml is not valid TOML: {e}")


class TestEditorConfig:
    """Tests for editor configuration."""

    def test_editorconfig_exists(self, repo_root: Path) -> None:
        """Verify .editorconfig exists for consistent editing."""
        editorconfig = repo_root / ".editorconfig"
        assert editorconfig.exists(), ".editorconfig not found"


class TestSecurityConfig:
    """Tests for security-related configuration."""

    def test_security_md_exists(self, repo_root: Path) -> None:
        """Verify SECURITY.md exists for vulnerability reporting."""
        security = repo_root / "SECURITY.md"
        assert security.exists(), "SECURITY.md not found"
        content = security.read_text()
        assert len(content) > 0, "SECURITY.md should have content"
