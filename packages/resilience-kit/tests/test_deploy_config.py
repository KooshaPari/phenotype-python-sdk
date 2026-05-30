"""Tests for deploy-kit config module."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from pheno_deploy_kit.config import DeployConfig, PackageDetector


class TestDeployConfig:
    """Tests for DeployConfig class."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary project directory."""
        return tmp_path

    def test_deploy_config_basic_init(self, temp_project: Path) -> None:
        """Test basic DeployConfig initialization."""
        config = DeployConfig(project_root=temp_project)
        assert config.project_root == temp_project.resolve()
        assert config.python_version == "3.10"
        assert isinstance(config.pheno_packages, set)
        assert isinstance(config.external_deps, set)

    def test_deploy_config_with_requirements(self, temp_project: Path) -> None:
        """Test DeployConfig with requirements.txt."""
        req_file = temp_project / "requirements.txt"
        req_file.write_text(
            "-e ../pheno-sdk/adapter-kit\n"
            "requests>=2.28.0\n"
            "# This is a comment\n"
        )

        config = DeployConfig(project_root=temp_project)
        assert "adapter-kit" in config.pheno_packages
        assert "requests" in config.external_deps

    def test_deploy_config_detect_python_version_from_pyproject(
        self, temp_project: Path
    ) -> None:
        """Test Python version detection from pyproject.toml."""
        pyproject = temp_project / "pyproject.toml"
        pyproject.write_text(
            '[project]\n'
            'requires-python = ">=3.11"\n'
        )

        config = DeployConfig(project_root=temp_project)
        assert config.python_version == "3.11"

    def test_deploy_config_detect_python_version_from_runtime(
        self, temp_project: Path
    ) -> None:
        """Test Python version detection from runtime.txt."""
        runtime = temp_project / "runtime.txt"
        runtime.write_text("python-3.12")

        config = DeployConfig(project_root=temp_project)
        assert config.python_version == "3.12"

    def test_deploy_config_detect_entry_point(self, temp_project: Path) -> None:
        """Test entry point detection."""
        # Create main.py
        (temp_project / "main.py").touch()

        config = DeployConfig(project_root=temp_project)
        assert config.entry_point == "main.py"

    def test_deploy_config_to_vercel_config(self, temp_project: Path) -> None:
        """Test Vercel configuration generation."""
        config = DeployConfig(project_root=temp_project)
        vercel_config = config.to_vercel_config()

        assert vercel_config["version"] == 2
        assert "builds" in vercel_config
        assert "routes" in vercel_config
        assert vercel_config["env"]["PYTHONPATH"] == "pheno_vendor"

    def test_deploy_config_to_docker_config(self, temp_project: Path) -> None:
        """Test Dockerfile generation."""
        config = DeployConfig(project_root=temp_project)
        dockerfile = config.to_docker_config()

        assert "FROM python" in dockerfile
        assert "pheno_vendor" in dockerfile
        assert "COPY" in dockerfile

    def test_deploy_config_to_lambda_config(self, temp_project: Path) -> None:
        """Test AWS Lambda configuration generation."""
        config = DeployConfig(project_root=temp_project)
        lambda_config = config.to_lambda_config()

        assert "runtime" in lambda_config
        assert "handler" in lambda_config
        assert "timeout" in lambda_config

    def test_deploy_config_to_railway_config(self, temp_project: Path) -> None:
        """Test Railway configuration generation."""
        config = DeployConfig(project_root=temp_project)
        railway_config = config.to_railway_config()

        assert "build" in railway_config
        assert "deploy" in railway_config

    def test_deploy_config_generate_build_script(self, temp_project: Path) -> None:
        """Test build script generation."""
        config = DeployConfig(project_root=temp_project)
        script = config.generate_build_script("docker")

        assert "#!/bin/bash" in script
        assert "pheno-sdk" in script or "Vendoring" in script

    def test_deploy_config_save_configs(self, temp_project: Path) -> None:
        """Test saving all configurations."""
        config = DeployConfig(project_root=temp_project)
        created_files = config.save_configs()

        assert len(created_files) == 4
        assert (temp_project / "vercel.json").exists()
        assert (temp_project / "Dockerfile").exists()
        assert (temp_project / "railway.json").exists()
        assert (temp_project / "build.sh").exists()


class TestPackageDetector:
    """Tests for PackageDetector class."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary project directory."""
        return tmp_path

    def test_package_detector_basic_init(self, temp_project: Path) -> None:
        """Test basic PackageDetector initialization."""
        detector = PackageDetector(project_root=temp_project)
        assert detector.project_root == temp_project.resolve()

    def test_detect_from_requirements(self, temp_project: Path) -> None:
        """Test detection from requirements.txt."""
        req_file = temp_project / "requirements.txt"
        req_file.write_text(
            "-e ../pheno-sdk/pydevkit\n"
            "-e ../pheno-sdk/adapter-kit\n"
        )

        detector = PackageDetector(project_root=temp_project)
        packages = detector.detect_from_requirements()

        assert "pydevkit" in packages
        assert "adapter-kit" in packages

    def test_detect_from_imports(self, temp_project: Path) -> None:
        """Test detection from Python imports."""
        # Create a Python file with imports
        py_file = temp_project / "test_module.py"
        py_file.write_text(
            "import pydevkit\n"
            "from adapter_kit import something\n"
        )

        detector = PackageDetector(project_root=temp_project)
        packages = detector.detect_from_imports()

        assert "pydevkit" in packages
        assert "adapter-kit" in packages

    def test_detect_all(self, temp_project: Path) -> None:
        """Test combined detection."""
        req_file = temp_project / "requirements.txt"
        req_file.write_text("-e ../pheno-sdk/pydevkit\n")

        py_file = temp_project / "test_module.py"
        py_file.write_text("from adapter_kit import something\n")

        detector = PackageDetector(project_root=temp_project)
        all_packages = detector.detect_all()

        assert "pydevkit" in all_packages
        assert "adapter-kit" in all_packages

    def test_detect_excludes_vendor_dirs(self, temp_project: Path) -> None:
        """Test that vendor directories are excluded."""
        # Create a Python file in a vendor directory
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()
        py_file = vendor_dir / "test.py"
        py_file.write_text("import some_package\n")

        detector = PackageDetector(project_root=temp_project)
        packages = detector.detect_from_imports()

        # Should not detect from vendor directory
        assert "some_package" not in packages
