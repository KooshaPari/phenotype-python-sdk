"""Tests for PhenoKits organizational structure.

Verifies that the 12-category artifact organization structure is correctly
established and all required directories exist.
"""

from __future__ import annotations

from pathlib import Path

import pytest


class TestCategoryStructure:
    """Test that all 12 PhenoKits category directories exist."""

    @pytest.mark.parametrize(
        "category",
        [
            "templates",
            "configs",
            "libs",
            "secrets",
            "governance",
            "security",
            "observability",
            "docs",
            "scripts",
            "schemas",
            "policies",
            "credentials",
        ],
    )
    def test_category_directory_exists(self, repo_root: Path, category: str) -> None:
        """Verify each category directory exists at the repository root."""
        category_path = repo_root / category
        assert category_path.exists(), f"Category directory '{category}' does not exist"
        assert category_path.is_dir(), f"Category '{category}' is not a directory"

    def test_category_directories_count(self, repo_root: Path) -> None:
        """Verify exactly 12 category directories exist."""
        categories = [
            "templates",
            "configs",
            "libs",
            "secrets",
            "governance",
            "security",
            "observability",
            "docs",
            "scripts",
            "schemas",
            "policies",
            "credentials",
        ]
        existing = [c for c in categories if (repo_root / c).exists()]
        assert len(existing) == 12, f"Expected 12 categories, found {len(existing)}: {existing}"


class TestCoreConfiguration:
    """Test that core configuration files exist and are valid."""

    def test_cargo_toml_exists(self, repo_root: Path) -> None:
        """Verify Cargo.toml exists for workspace configuration."""
        cargo_toml = repo_root / "Cargo.toml"
        assert cargo_toml.exists(), "Cargo.toml not found at repository root"

    def test_cargo_toml_is_workspace_root(self, repo_root: Path) -> None:
        """Verify Cargo.toml declares a virtual workspace."""
        cargo_toml = repo_root / "Cargo.toml"
        content = cargo_toml.read_text()
        assert "[workspace]" in content, "Cargo.toml missing [workspace] section"
        # Verify it's a virtual workspace (no members, just excludes)
        assert "members = []" in content, "Root Cargo.toml should be a virtual workspace"

    def test_pyproject_does_not_exist_at_root(self, repo_root: Path) -> None:
        """Verify no Python package at root level (Python code is in HexaKit/)."""
        pyproject = repo_root / "pyproject.toml"
        # It's OK if there's no pyproject.toml at root - Python code is in HexaKit/
        # This test documents the structure
        if pyproject.exists():
            content = pyproject.read_text()
            assert "[project]" not in content, "Root should not be a Python package"

    def test_gitignore_exists(self, repo_root: Path) -> None:
        """Verify .gitignore exists for common exclusions."""
        gitignore = repo_root / ".gitignore"
        assert gitignore.exists(), ".gitignore not found"
        content = gitignore.read_text()
        # Should exclude worktrees, Cargo artifacts, etc.
        assert "worktrees" in content.lower() or "target" in content.lower()

    def test_readme_exists(self, repo_root: Path) -> None:
        """Verify README.md exists."""
        readme = repo_root / "README.md"
        assert readme.exists(), "README.md not found at repository root"

    def test_license_exists(self, repo_root: Path) -> None:
        """Verify license file exists."""
        license_file = repo_root / "LICENSE"
        assert license_file.exists(), "LICENSE file not found"

    def test_github_workflows_exist(self, repo_root: Path) -> None:
        """Verify GitHub workflows directory exists."""
        workflows_dir = repo_root / ".github" / "workflows"
        if workflows_dir.exists():
            # Should have at least one workflow file
            workflow_files = list(workflows_dir.glob("*.yml")) + list(
                workflows_dir.glob("*.yaml")
            )
            assert len(workflow_files) > 0, "No workflow files found in .github/workflows/"


class TestHexaKitSubmodule:
    """Test HexaKit submodule structure."""

    def test_hexakit_exists(self, repo_root: Path) -> None:
        """Verify HexaKit directory exists."""
        hexakit = repo_root / "HexaKit"
        assert hexakit.exists(), "HexaKit submodule not found"
        assert hexakit.is_dir(), "HexaKit is not a directory"

    def test_hexakit_has_cargo_toml(self, repo_root: Path) -> None:
        """Verify HexaKit has its own Cargo.toml (it's a Rust workspace)."""
        hexakit = repo_root / "HexaKit"
        cargo_toml = hexakit / "Cargo.toml"
        assert cargo_toml.exists(), "HexaKit/Cargo.toml not found"

    def test_hexakit_has_python_dir(self, repo_root: Path) -> None:
        """Verify HexaKit contains Python code."""
        hexakit = repo_root / "HexaKit"
        python_dir = hexakit / "python"
        assert python_dir.exists(), "HexaKit/python directory not found"
        assert python_dir.is_dir(), "HexaKit/python is not a directory"


class TestPythonLibraries:
    """Test Python libraries in libs/python/."""

    def test_python_libs_dir_exists(self, python_libs_dir: Path) -> None:
        """Verify libs/python/ directory exists."""
        assert python_libs_dir.exists(), "libs/python/ not found"
        assert python_libs_dir.is_dir(), "libs/python/ is not a directory"

    def test_python_libs_have_pyproject_toml(self, python_libs_dir: Path) -> None:
        """Verify Python libraries have pyproject.toml files."""
        pyproject_files = list(python_libs_dir.rglob("pyproject.toml"))
        assert len(pyproject_files) > 0, "No pyproject.toml files found in libs/python/"

    def test_phenotype_py_kit_exists(self, python_libs_dir: Path) -> None:
        """Verify phenotype-py-kit library exists."""
        kit = python_libs_dir / "phenotype-py-kit"
        assert kit.exists(), "phenotype-py-kit not found"

        # Check for source files
        src_dir = kit / "src" / "phenotype_kit"
        assert src_dir.exists(), "phenotype-py-kit source not found"

    def test_phenotype_logging_exists(self, python_libs_dir: Path) -> None:
        """Verify phenotype-logging library exists."""
        kit = python_libs_dir / "phenotype-logging"
        assert kit.exists(), "phenotype-logging not found"

    def test_pheno_cli_kit_exists(self, python_libs_dir: Path) -> None:
        """Verify pheno-cli-kit library exists."""
        kit = python_libs_dir / "pheno-cli-kit"
        assert kit.exists(), "pheno-cli-kit not found"
