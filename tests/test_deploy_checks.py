"""Tests for deploy-kit checks module."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pheno_deploy_kit.checks import VendorChecker, check_freshness


class TestVendorChecker:
    """Tests for VendorChecker class."""

    @pytest.fixture
    def temp_project(self, tmp_path: Path) -> Path:
        """Create a temporary project directory."""
        return tmp_path

    def test_initialization_default(self) -> None:
        """Test VendorChecker initialization with defaults."""
        checker = VendorChecker()

        assert checker.project_root is not None
        assert checker.quiet is False
        assert checker.vendor_dir == checker.project_root / "pheno_vendor"
        assert checker.requirements_file == checker.project_root / "requirements.txt"

    def test_initialization_custom(self, temp_project: Path) -> None:
        """Test VendorChecker initialization with custom project root."""
        checker = VendorChecker(project_root=temp_project, quiet=True)

        assert checker.project_root == temp_project
        assert checker.quiet is True

    def test_check_vendor_exists_false(self, temp_project: Path) -> None:
        """Test check_vendor_exists when vendor dir doesn't exist."""
        checker = VendorChecker(project_root=temp_project)

        assert checker.check_vendor_exists() is False

    def test_check_vendor_exists_true(self, temp_project: Path) -> None:
        """Test check_vendor_exists when vendor dir exists."""
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()

        checker = VendorChecker(project_root=temp_project)
        assert checker.check_vendor_exists() is True

    def test_check_requirements_exist_false(self, temp_project: Path) -> None:
        """Test check_requirements_exist when requirements.txt doesn't exist."""
        checker = VendorChecker(project_root=temp_project)

        assert checker.check_requirements_exist() is False

    def test_check_requirements_exist_true(self, temp_project: Path) -> None:
        """Test check_requirements_exist when requirements.txt exists."""
        requirements_file = temp_project / "requirements.txt"
        requirements_file.write_text("requests>=2.28.0\n")

        checker = VendorChecker(project_root=temp_project)
        assert checker.check_requirements_exist() is True

    def test_get_vendor_mtime_none(self, temp_project: Path) -> None:
        """Test get_vendor_mtime when vendor dir doesn't exist."""
        checker = VendorChecker(project_root=temp_project)

        assert checker.get_vendor_mtime() is None

    def test_get_vendor_mtime_returns_time(self, temp_project: Path) -> None:
        """Test get_vendor_mtime returns valid timestamp."""
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()

        checker = VendorChecker(project_root=temp_project)
        mtime = checker.get_vendor_mtime()

        assert mtime is not None
        assert mtime > 0

    def test_get_requirements_mtime_none(self, temp_project: Path) -> None:
        """Test get_requirements_mtime when requirements.txt doesn't exist."""
        checker = VendorChecker(project_root=temp_project)

        assert checker.get_requirements_mtime() is None

    def test_get_requirements_mtime_returns_time(self, temp_project: Path) -> None:
        """Test get_requirements_mtime returns valid timestamp."""
        requirements_file = temp_project / "requirements.txt"
        requirements_file.write_text("requests>=2.28.0\n")

        checker = VendorChecker(project_root=temp_project)
        mtime = checker.get_requirements_mtime()

        assert mtime is not None
        assert mtime > 0

    def test_is_vendoring_stale_no_vendor_dir(self, temp_project: Path) -> None:
        """Test is_vendoring_stale when vendor dir doesn't exist."""
        requirements_file = temp_project / "requirements.txt"
        requirements_file.write_text("requests>=2.28.0\n")

        prod_file = temp_project / "requirements-prod.txt"
        prod_file.write_text("flask>=2.0.0\n")

        checker = VendorChecker(project_root=temp_project)
        is_stale, reason = checker.is_vendoring_stale()

        assert is_stale is True
        assert "does not exist" in reason

    def test_is_vendoring_stale_no_requirements(self, temp_project: Path) -> None:
        """Test is_vendoring_stale when requirements.txt doesn't exist."""
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()

        checker = VendorChecker(project_root=temp_project)
        is_stale, reason = checker.is_vendoring_stale()

        assert is_stale is False
        assert "not found" in reason

    def test_is_vendoring_stale_no_prod_requirements(self, temp_project: Path) -> None:
        """Test is_vendoring_stale when requirements-prod.txt doesn't exist."""
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()

        requirements_file = temp_project / "requirements.txt"
        requirements_file.write_text("requests>=2.28.0\n")

        checker = VendorChecker(project_root=temp_project)
        is_stale, reason = checker.is_vendoring_stale()

        assert is_stale is True
        assert "requirements-prod.txt" in reason

    def test_is_vendoring_stale_empty_vendor(self, temp_project: Path) -> None:
        """Test is_vendoring_stale when vendor dir is empty."""
        requirements_file = temp_project / "requirements.txt"
        requirements_file.write_text("requests>=2.28.0\n")

        prod_file = temp_project / "requirements-prod.txt"
        prod_file.write_text("flask>=2.0.0\n")

        # Create vendor dir last so it's older than requirements files
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()

        checker = VendorChecker(project_root=temp_project)
        is_stale, reason = checker.is_vendoring_stale()

        assert is_stale is True
        assert "empty" in reason.lower()

    def test_is_vendoring_stale_up_to_date(self, temp_project: Path) -> None:
        """Test is_vendoring_stale when vendor is up-to-date."""
        import os
        import time

        # Create vendor dir first
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()

        package_dir = vendor_dir / "pheno_core"
        package_dir.mkdir()

        requirements_file = temp_project / "requirements.txt"
        requirements_file.write_text("requests>=2.28.0\n")

        prod_file = temp_project / "requirements-prod.txt"
        prod_file.write_text("flask>=2.0.0\n")

        # Ensure vendor dir is newer than requirements by touching vendor
        time.sleep(0.1)
        os.utime(vendor_dir, None)

        checker = VendorChecker(project_root=temp_project)
        is_stale, reason = checker.is_vendoring_stale()

        assert is_stale is False
        assert "up-to-date" in reason.lower()

    def test_is_vendoring_stale_requirements_newer(
        self, temp_project: Path
    ) -> None:
        """Test is_vendoring_stale when requirements.txt is newer."""
        vendor_dir = temp_project / "pheno_vendor"
        vendor_dir.mkdir()

        package_dir = vendor_dir / "pheno_core"
        package_dir.mkdir()

        requirements_file = temp_project / "requirements.txt"
        requirements_file.write_text("requests>=2.28.0\n")

        prod_file = temp_project / "requirements-prod.txt"
        prod_file.write_text("flask>=2.0.0\n")

        # Make requirements.txt newer
        import time

        time.sleep(0.1)
        requirements_file.touch()

        checker = VendorChecker(project_root=temp_project)
        is_stale, reason = checker.is_vendoring_stale()

        assert is_stale is True
        assert "newer" in reason.lower()

    @patch("subprocess.run")
    def test_run_vendor_setup_pheno_vendor_not_found(
        self, mock_run: pytest.Mock, temp_project: Path
    ) -> None:
        """Test run_vendor_setup when pheno-vendor is not found."""
        mock_run.side_effect = FileNotFoundError()

        checker = VendorChecker(project_root=temp_project, quiet=True)
        result = checker.run_vendor_setup()

        assert result is False

    @patch("subprocess.run")
    def test_run_vendor_setup_success(
        self, mock_run: pytest.Mock, temp_project: Path
    ) -> None:
        """Test run_vendor_setup successful execution."""
        mock_result = MagicMock()
        mock_result.returncode = 0

        mock_run.return_value = mock_result

        checker = VendorChecker(project_root=temp_project, quiet=True)
        result = checker.run_vendor_setup()

        assert result is True

    @patch("subprocess.run")
    def test_run_vendor_setup_failure(
        self, mock_run: pytest.Mock, temp_project: Path
    ) -> None:
        """Test run_vendor_setup failed execution."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error message"

        mock_run.return_value = mock_result

        checker = VendorChecker(project_root=temp_project, quiet=True)
        result = checker.run_vendor_setup()

        assert result is False


class TestCheckFreshness:
    """Tests for check_freshness function."""

    @patch("pheno_deploy_kit.checks.VendorChecker")
    def test_check_freshness_passes_args(
        self, mock_checker_class: pytest.Mock, tmp_path: Path
    ) -> None:
        """Test check_freshness passes arguments correctly."""
        mock_checker = MagicMock()
        mock_checker.check_and_report.return_value = 0
        mock_checker_class.return_value = mock_checker

        result = check_freshness(
            project_root=tmp_path, auto_vendor=True, force=True, quiet=True,
        )

        mock_checker_class.assert_called_once_with(
            project_root=tmp_path, quiet=True,
        )
        mock_checker.check_and_report.assert_called_once_with(
            auto_vendor=True, force=True,
        )
        assert result == 0
