"""Tests for deploy-kit utils module."""

from __future__ import annotations

from pathlib import Path

import pytest

from pheno_deploy_kit.utils import (
    BuildHookGenerator,
    DeploymentValidator,
    EnvironmentManager,
    PlatformDetector,
    PlatformInfo,
)


class TestPlatformDetector:
    """Tests for PlatformDetector class."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary project directory."""
        # Clean up any platform files that might exist
        platform_files = [
            "vercel.json", ".vercel", "Dockerfile", "docker-compose.yml",
            ".dockerignore", "fly.toml", "railway.json", "railway.toml",
            "Procfile", "app.json", "serverless.yml", "template.yaml",
            ".aws-sam", "wrangler.toml"
        ]
        for f in platform_files:
            fp = tmp_path / f
            if fp.exists():
                fp.unlink()
        return tmp_path

    def test_platform_detector_basic_init(self, temp_project: Path) -> None:
        """Test basic PlatformDetector initialization."""
        detector = PlatformDetector(project_root=temp_project)
        assert detector.project_root == temp_project.resolve()

    def test_detect_no_platform(self, temp_project: Path) -> None:
        """Test detection with no platform files."""
        detector = PlatformDetector(project_root=temp_project)
        platform = detector.detect()
        assert platform == "docker"  # Default fallback

    def test_detect_vercel(self, temp_project: Path) -> None:
        """Test Vercel detection."""
        (temp_project / "vercel.json").touch()

        detector = PlatformDetector(project_root=temp_project)
        platform = detector.detect()
        assert platform == "vercel"

    def test_detect_docker(self, temp_project: Path) -> None:
        """Test Docker detection."""
        (temp_project / "Dockerfile").touch()

        detector = PlatformDetector(project_root=temp_project)
        platform = detector.detect()
        assert platform == "docker"

    def test_detect_fly(self, temp_project: Path) -> None:
        """Test Fly.io detection."""
        (temp_project / "fly.toml").touch()

        detector = PlatformDetector(project_root=temp_project)
        platform = detector.detect()
        assert platform == "fly"

    def test_detect_railway(self, temp_project: Path) -> None:
        """Test Railway detection."""
        (temp_project / "railway.json").touch()

        detector = PlatformDetector(project_root=temp_project)
        platform = detector.detect()
        assert platform == "railway"

    def test_detect_all_returns_list(self, temp_project: Path) -> None:
        """Test detect_all returns a list of PlatformInfo."""
        (temp_project / "Dockerfile").touch()
        (temp_project / "docker-compose.yml").touch()

        detector = PlatformDetector(project_root=temp_project)
        results = detector.detect_all()

        assert isinstance(results, list)
        assert all(isinstance(r, PlatformInfo) for r in results)

    def test_detect_all_sorted_by_confidence(self, temp_project: Path) -> None:
        """Test detect_all returns results sorted by confidence."""
        (temp_project / "Dockerfile").touch()

        detector = PlatformDetector(project_root=temp_project)
        results = detector.detect_all()

        # Results should be sorted by confidence descending
        if len(results) > 1:
            for i in range(len(results) - 1):
                assert results[i].confidence >= results[i + 1].confidence


class TestBuildHookGenerator:
    """Tests for BuildHookGenerator class."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary project directory."""
        return tmp_path

    def test_build_hook_generator_init(self, temp_project: Path) -> None:
        """Test BuildHookGenerator initialization."""
        generator = BuildHookGenerator(project_root=temp_project)
        assert generator.project_root == temp_project.resolve()

    def test_generate_vercel(self, temp_project: Path) -> None:
        """Test Vercel build hook generation."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("vercel")

        assert "#!/bin/bash" in hook
        assert "pheno-vendor" in hook or "Vendoring" in hook

    def test_generate_docker(self, temp_project: Path) -> None:
        """Test Docker build hook generation."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("docker")

        assert "FROM python" in hook

    def test_generate_lambda(self, temp_project: Path) -> None:
        """Test Lambda build hook generation."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("lambda")

        assert "AWS Lambda" in hook or "Lambda" in hook

    def test_generate_railway(self, temp_project: Path) -> None:
        """Test Railway build hook generation."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("railway")

        assert "pheno-vendor" in hook or "Railway" in hook

    def test_generate_heroku(self, temp_project: Path) -> None:
        """Test Heroku build hook generation."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("heroku")

        assert "Heroku" in hook or "pheno-vendor" in hook

    def test_generate_fly(self, temp_project: Path) -> None:
        """Test Fly.io build hook generation."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("fly")

        assert "Fly" in hook or "python" in hook

    def test_generate_cloudflare(self, temp_project: Path) -> None:
        """Test Cloudflare build hook generation."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("cloudflare")

        assert "Cloudflare" in hook or "pheno-vendor" in hook

    def test_generate_unknown_platform(self, temp_project: Path) -> None:
        """Test generation for unknown platform falls back to generic."""
        generator = BuildHookGenerator(project_root=temp_project)
        hook = generator.generate("unknown_platform")

        assert "#!/bin/bash" in hook
        assert "Build complete" in hook or "Build" in hook


class TestDeploymentValidator:
    """Tests for DeploymentValidator class."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary project directory."""
        return tmp_path

    def test_deployment_validator_init(self, temp_project: Path) -> None:
        """Test DeploymentValidator initialization."""
        validator = DeploymentValidator(project_root=temp_project)
        assert validator.project_root == temp_project.resolve()

    def test_validate_no_vendor_dir(self, temp_project: Path) -> None:
        """Test validation fails when vendor directory doesn't exist."""
        validator = DeploymentValidator(project_root=temp_project)
        success, errors = validator.validate()

        assert success is False
        assert any("Vendor directory not found" in e for e in errors)

    def test_validate_with_vendor_dir(self, temp_project: Path) -> None:
        """Test validation with proper vendor directory."""
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()
        (vendor_dir / "__init__.py").touch()

        # Create requirements-prod.txt
        (temp_project / "requirements-prod.txt").touch()

        # Create sitecustomize.py
        (temp_project / "sitecustomize.py").touch()

        validator = DeploymentValidator(project_root=temp_project)
        success, errors = validator.validate()

        assert success is True
        assert len(errors) == 0


class TestEnvironmentManager:
    """Tests for EnvironmentManager class."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary project directory."""
        return tmp_path

    def test_environment_manager_init(self, temp_project: Path) -> None:
        """Test EnvironmentManager initialization."""
        manager = EnvironmentManager(project_root=temp_project)
        assert manager.project_root == temp_project.resolve()

    def test_generate_env_template(self, temp_project: Path) -> None:
        """Test environment template generation."""
        manager = EnvironmentManager(project_root=temp_project)
        template = manager.generate_env_template()

        assert "Environment Variables Template" in template
        assert "PYTHONPATH" in template

    def test_validate_env_no_file(self, temp_project: Path) -> None:
        """Test validation fails when no .env file exists."""
        manager = EnvironmentManager(project_root=temp_project)
        success, missing = manager.validate_env("vercel")

        assert success is False
        assert "No .env file found" in missing

    def test_validate_env_with_file(self, temp_project: Path) -> None:
        """Test validation with .env file."""
        env_file = temp_project / ".env"
        env_file.write_text("PYTHONPATH=pheno_vendor\nDEBUG=true\n")

        manager = EnvironmentManager(project_root=temp_project)
        success, missing = manager.validate_env("vercel")

        assert success is True
        assert len(missing) == 0
