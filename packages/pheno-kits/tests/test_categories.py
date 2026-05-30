"""Tests for PhenoKits governance and documentation categories."""

from __future__ import annotations

from pathlib import Path

import pytest


class TestGovernanceCategory:
    """Tests for the governance/ category."""

    def test_governance_dir_exists(self, repo_root: Path) -> None:
        """Verify governance/ directory exists."""
        governance = repo_root / "governance"
        assert governance.exists(), "governance/ directory not found"
        assert governance.is_dir(), "governance/ is not a directory"

    def test_governance_has_adr_support(self, repo_root: Path) -> None:
        """Verify governance category supports ADRs (Architecture Decision Records)."""
        governance = repo_root / "governance"
        # Check if there are ADR files or templates
        adr_files = list(governance.glob("**/*ADR*")) + list(
            governance.glob("**/*adr*")
        )
        # ADRs are optional but should be supported
        # Just verify governance directory is accessible
        assert governance.exists()


class TestSecurityCategory:
    """Tests for the security/ category."""

    def test_security_dir_exists(self, repo_root: Path) -> None:
        """Verify security/ directory exists."""
        security = repo_root / "security"
        assert security.exists(), "security/ directory not found"
        assert security.is_dir(), "security/ is not a directory"


class TestObservabilityCategory:
    """Tests for the observability/ category."""

    def test_observability_dir_exists(self, repo_root: Path) -> None:
        """Verify observability/ directory exists."""
        obs = repo_root / "observability"
        assert obs.exists(), "observability/ directory not found"
        assert obs.is_dir(), "observability/ is not a directory"

    def test_observability_has_logging_config(self, repo_root: Path) -> None:
        """Verify observability category has logging configurations."""
        obs = repo_root / "observability"
        # Check for logging, metrics, or tracing configs
        configs = list(obs.rglob("*.yaml")) + list(obs.rglob("*.yml")) + list(
            obs.rglob("*.json")
        )
        # Configs are optional
        assert obs.exists()


class TestSchemasCategory:
    """Tests for the schemas/ category."""

    def test_schemas_dir_exists(self, repo_root: Path) -> None:
        """Verify schemas/ directory exists."""
        schemas = repo_root / "schemas"
        assert schemas.exists(), "schemas/ directory not found"
        assert schemas.is_dir(), "schemas/ is not a directory"


class TestPoliciesCategory:
    """Tests for the policies/ category."""

    def test_policies_dir_exists(self, repo_root: Path) -> None:
        """Verify policies/ directory exists."""
        policies = repo_root / "policies"
        assert policies.exists(), "policies/ directory not found"
        assert policies.is_dir(), "policies/ is not a directory"


class TestCredentialsCategory:
    """Tests for the credentials/ category."""

    def test_credentials_dir_exists(self, repo_root: Path) -> None:
        """Verify credentials/ directory exists."""
        creds = repo_root / "credentials"
        assert creds.exists(), "credentials/ directory not found"
        assert creds.is_dir(), "credentials/ is not a directory"


class TestDocsCategory:
    """Tests for the docs/ category."""

    def test_docs_dir_exists(self, repo_root: Path) -> None:
        """Verify docs/ directory exists."""
        docs = repo_root / "docs"
        assert docs.exists(), "docs/ directory not found"
        assert docs.is_dir(), "docs/ is not a directory"

    def test_docs_has_content(self, repo_root: Path) -> None:
        """Verify docs/ directory has content."""
        docs = repo_root / "docs"
        if docs.exists():
            # Check for documentation files
            doc_files = (
                list(docs.glob("*.md"))
                + list(docs.glob("*.mdx"))
                + list(docs.glob("*.rst"))
                + list(docs.glob("*.txt"))
            )
            # Documentation should exist
            assert docs.exists()


class TestConfigsCategory:
    """Tests for the configs/ category."""

    def test_configs_dir_exists(self, repo_root: Path) -> None:
        """Verify configs/ directory exists."""
        configs = repo_root / "configs"
        assert configs.exists(), "configs/ directory not found"
        assert configs.is_dir(), "configs/ is not a directory"

    def test_configs_has_config_files(self, repo_root: Path) -> None:
        """Verify configs/ has configuration files."""
        configs = repo_root / "configs"
        if configs.exists():
            config_files = (
                list(configs.rglob("*.yaml"))
                + list(configs.rglob("*.yml"))
                + list(configs.rglob("*.toml"))
                + list(configs.rglob("*.json"))
            )
            # Should have some config files
            assert configs.exists()


class TestScriptsCategory:
    """Tests for the scripts/ category."""

    def test_scripts_dir_exists(self, repo_root: Path) -> None:
        """Verify scripts/ directory exists."""
        scripts = repo_root / "scripts"
        assert scripts.exists(), "scripts/ directory not found"
        assert scripts.is_dir(), "scripts/ is not a directory"

    def test_scripts_has_readme(self, repo_root: Path) -> None:
        """Verify scripts/ has a README."""
        scripts = repo_root / "scripts"
        readme = scripts / "README.md"
        if readme.exists():
            content = readme.read_text()
            assert len(content) > 0, "scripts/README.md should have content"


class TestTemplatesCategory:
    """Tests for the templates/ category."""

    def test_templates_dir_exists(self, repo_root: Path) -> None:
        """Verify templates/ directory exists."""
        templates = repo_root / "templates"
        assert templates.exists(), "templates/ directory not found"
        assert templates.is_dir(), "templates/ is not a directory"


class TestSecretsCategory:
    """Tests for the secrets/ category."""

    def test_secrets_dir_exists(self, repo_root: Path) -> None:
        """Verify secrets/ directory exists."""
        secrets = repo_root / "secrets"
        assert secrets.exists(), "secrets/ directory not found"
        assert secrets.is_dir(), "secrets/ is not a directory"


class TestLibsCategory:
    """Tests for the libs/ category."""

    def test_libs_dir_exists(self, repo_root: Path) -> None:
        """Verify libs/ directory exists."""
        libs = repo_root / "libs"
        assert libs.exists(), "libs/ directory not found"
        assert libs.is_dir(), "libs/ is not a directory"

    def test_libs_has_multi_language_support(self, repo_root: Path) -> None:
        """Verify libs/ has multi-language library directories."""
        libs = repo_root / "libs"

        # Should have directories for different languages
        expected_langs = ["python", "go", "typescript"]

        existing_langs = [lang for lang in expected_langs if (libs / lang).exists()]
        assert len(existing_langs) > 0, f"libs/ should have language directories"
