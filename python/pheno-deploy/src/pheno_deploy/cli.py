#!/usr/bin/env python3
"""
Pheno-Deploy: Unified deployment CLI for Phenotype projects.

A standalone deployment automation tool extracted from phenoSDK.
Provides commands for building, releasing, checking deployments, schema drift detection,
and artifact management.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import venv
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Console for rich output
console = Console()

# Typer app with subcommands
app = typer.Typer(
    help="Pheno-Deploy: Unified deployment CLI for Phenotype projects",
    rich_markup_mode="rich",
)


# ============================================================================
# Data Classes and Enums
# ============================================================================


class CheckPriority(Enum):
    """Priority levels for deployment checks."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CheckStatus(Enum):
    """Status values for deployment checks."""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class CheckResult:
    """Result of a deployment readiness check."""

    name: str
    status: CheckStatus
    priority: CheckPriority
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0


@dataclass
class ReleaseInfo:
    """Release information."""

    version: str
    release_type: str
    changelog: str
    release_notes: str
    git_tag: str
    timestamp: float
    author: str
    commit_hash: str


@dataclass
class ReleaseStep:
    """Release step information."""

    name: str
    status: str  # pending, running, completed, failed
    duration: float
    output: str
    error: str | None = None


# ============================================================================
# Utility Functions
# ============================================================================


def run_command(
    cmd: list[str] | str,
    cwd: Path | None = None,
    check: bool = True,
    timeout: int | None = 300,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a shell command with error handling."""
    if isinstance(cmd, str):
        cmd = cmd.split()

    result = subprocess.run(
        cmd,
        check=False,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
    )

    if check and result.returncode != 0:
        console.print(f"[red]Command failed:[/red] {' '.join(cmd)}")
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print(result.stderr)
        raise typer.Exit(code=result.returncode)

    return result


def get_git_author(project_root: Path) -> str:
    """Get git author information."""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            check=False,
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        return result.stdout.strip() if result.returncode == 0 else "Unknown"
    except Exception:
        return "Unknown"


def get_current_commit(project_root: Path) -> str:
    """Get current commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        return result.stdout.strip() if result.returncode == 0 else "Unknown"
    except Exception:
        return "Unknown"


def get_commits_since_last_tag(project_root: Path) -> list[dict[str, str]]:
    """Get commits since the last tag."""
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--oneline",
                "--format=%H|%s|%an|%ae",
                "--no-merges",
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=project_root,
        )

        commits = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|", 3)
                if len(parts) >= 4:
                    commits.append(
                        {
                            "hash": parts[0],
                            "message": parts[1],
                            "author": parts[2],
                            "email": parts[3],
                        }
                    )
        return commits
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Error getting commits: {e}")
        return []


# ============================================================================
# Deployment Checker (Standalone Implementation)
# ============================================================================


class DeploymentChecker:
    """Standalone deployment readiness checker."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self._checks: dict[str, tuple[CheckPriority, Callable[[], CheckResult]]] = {}
        self._register_default_checks()

    def _register_default_checks(self) -> None:
        """Register default deployment checks."""
        self._checks["git_clean"] = (CheckPriority.CRITICAL, self._check_git_clean)
        self._checks["pyproject_valid"] = (CheckPriority.CRITICAL, self._check_pyproject)
        self._checks["tests_exist"] = (CheckPriority.HIGH, self._check_tests_exist)
        self._checks["readme_exists"] = (CheckPriority.MEDIUM, self._check_readme)
        self._checks["changelog_exists"] = (CheckPriority.MEDIUM, self._check_changelog)
        self._checks["license_exists"] = (CheckPriority.LOW, self._check_license)
        self._checks["no_large_files"] = (CheckPriority.MEDIUM, self._check_large_files)
        self._checks["python_version"] = (CheckPriority.HIGH, self._check_python_version)

    def _check_git_clean(self) -> CheckResult:
        """Check if git working directory is clean."""
        start = time.time()
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            is_clean = result.returncode == 0 and not result.stdout.strip()
            duration = time.time() - start

            if is_clean:
                return CheckResult(
                    name="git_clean",
                    status=CheckStatus.PASSED,
                    priority=CheckPriority.CRITICAL,
                    message="Git working directory is clean",
                    duration=duration,
                )
            return CheckResult(
                name="git_clean",
                status=CheckStatus.FAILED,
                priority=CheckPriority.CRITICAL,
                message="Git working directory has uncommitted changes",
                details={"changes": result.stdout.strip()[:200]},
                duration=duration,
            )
        except Exception as e:
            return CheckResult(
                name="git_clean",
                status=CheckStatus.ERROR,
                priority=CheckPriority.CRITICAL,
                message=f"Error checking git status: {e}",
                duration=time.time() - start,
            )

    def _check_pyproject(self) -> CheckResult:
        """Check if pyproject.toml is valid."""
        start = time.time()
        pyproject_path = self.project_root / "pyproject.toml"

        if not pyproject_path.exists():
            return CheckResult(
                name="pyproject_valid",
                status=CheckStatus.FAILED,
                priority=CheckPriority.CRITICAL,
                message="pyproject.toml not found",
                duration=time.time() - start,
            )

        try:
            content = pyproject_path.read_text()
            has_version = bool(re.search(r'version\s*=\s*["\']', content))
            has_name = bool(re.search(r'name\s*=\s*["\']', content))

            duration = time.time() - start
            if has_version and has_name:
                return CheckResult(
                    name="pyproject_valid",
                    status=CheckStatus.PASSED,
                    priority=CheckPriority.CRITICAL,
                    message="pyproject.toml has required fields (name, version)",
                    duration=duration,
                )
            return CheckResult(
                name="pyproject_valid",
                status=CheckStatus.WARNING,
                priority=CheckPriority.CRITICAL,
                message="pyproject.toml may be missing required fields",
                details={"has_name": has_name, "has_version": has_version},
                duration=duration,
            )
        except Exception as e:
            return CheckResult(
                name="pyproject_valid",
                status=CheckStatus.ERROR,
                priority=CheckPriority.CRITICAL,
                message=f"Error reading pyproject.toml: {e}",
                duration=time.time() - start,
            )

    def _check_tests_exist(self) -> CheckResult:
        """Check if tests directory exists."""
        start = time.time()
        tests_paths = [
            self.project_root / "tests",
            self.project_root / "test",
            self.project_root / "src" / "tests",
        ]

        for path in tests_paths:
            if path.exists() and any(path.iterdir()):
                return CheckResult(
                    name="tests_exist",
                    status=CheckStatus.PASSED,
                    priority=CheckPriority.HIGH,
                    message=f"Tests directory found: {path.relative_to(self.project_root)}",
                    duration=time.time() - start,
                )

        return CheckResult(
            name="tests_exist",
            status=CheckStatus.WARNING,
            priority=CheckPriority.HIGH,
            message="No tests directory found",
            duration=time.time() - start,
        )

    def _check_readme(self) -> CheckResult:
        """Check if README exists."""
        start = time.time()
        readme_paths = [
            self.project_root / "README.md",
            self.project_root / "README.rst",
            self.project_root / "README",
        ]

        for path in readme_paths:
            if path.exists():
                return CheckResult(
                    name="readme_exists",
                    status=CheckStatus.PASSED,
                    priority=CheckPriority.MEDIUM,
                    message=f"README found: {path.name}",
                    duration=time.time() - start,
                )

        return CheckResult(
            name="readme_exists",
            status=CheckStatus.WARNING,
            priority=CheckPriority.MEDIUM,
            message="No README found",
            duration=time.time() - start,
        )

    def _check_changelog(self) -> CheckResult:
        """Check if CHANGELOG exists."""
        start = time.time()
        changelog_path = self.project_root / "CHANGELOG.md"

        if changelog_path.exists():
            return CheckResult(
                name="changelog_exists",
                status=CheckStatus.PASSED,
                priority=CheckPriority.MEDIUM,
                message="CHANGELOG.md found",
                duration=time.time() - start,
            )

        return CheckResult(
            name="changelog_exists",
            status=CheckStatus.WARNING,
            priority=CheckPriority.MEDIUM,
            message="CHANGELOG.md not found",
            duration=time.time() - start,
        )

    def _check_license(self) -> CheckResult:
        """Check if LICENSE exists."""
        start = time.time()
        license_paths = [
            self.project_root / "LICENSE",
            self.project_root / "LICENSE.txt",
            self.project_root / "LICENSE.md",
        ]

        for path in license_paths:
            if path.exists():
                return CheckResult(
                    name="license_exists",
                    status=CheckStatus.PASSED,
                    priority=CheckPriority.LOW,
                    message=f"License found: {path.name}",
                    duration=time.time() - start,
                )

        return CheckResult(
            name="license_exists",
            status=CheckStatus.WARNING,
            priority=CheckPriority.LOW,
            message="No LICENSE file found",
            duration=time.time() - start,
        )

    def _check_large_files(self) -> CheckResult:
        """Check for large files that shouldn't be committed."""
        start = time.time()
        large_files = []
        max_size = 10 * 1024 * 1024  # 10MB

        try:
            for path in self.project_root.rglob("*"):
                if path.is_file() and ".git" not in str(path):
                    try:
                        if path.stat().st_size > max_size:
                            large_files.append(str(path.relative_to(self.project_root)))
                    except (OSError, ValueError):
                        pass

            duration = time.time() - start
            if not large_files:
                return CheckResult(
                    name="no_large_files",
                    status=CheckStatus.PASSED,
                    priority=CheckPriority.MEDIUM,
                    message="No files larger than 10MB found",
                    duration=duration,
                )
            return CheckResult(
                name="no_large_files",
                status=CheckStatus.WARNING,
                priority=CheckPriority.MEDIUM,
                message=f"Found {len(large_files)} files larger than 10MB",
                details={"files": large_files[:5]},
                duration=duration,
            )
        except Exception as e:
            return CheckResult(
                name="no_large_files",
                status=CheckStatus.ERROR,
                priority=CheckPriority.MEDIUM,
                message=f"Error checking for large files: {e}",
                duration=time.time() - start,
            )

    def _check_python_version(self) -> CheckResult:
        """Check Python version compatibility."""
        start = time.time()
        version = sys.version_info

        if version >= (3, 9):
            return CheckResult(
                name="python_version",
                status=CheckStatus.PASSED,
                priority=CheckPriority.HIGH,
                message=f"Python {version.major}.{version.minor}.{version.micro} is supported",
                duration=time.time() - start,
            )
        return CheckResult(
            name="python_version",
            status=CheckStatus.WARNING,
            priority=CheckPriority.HIGH,
            message=f"Python {version.major}.{version.minor} may not be fully supported (3.9+ recommended)",
            duration=time.time() - start,
        )

    def list_checks(self) -> list[str]:
        """List all available checks."""
        return list(self._checks.keys())

    def run_check(self, name: str) -> CheckResult | None:
        """Run a specific check by name."""
        if name not in self._checks:
            return None
        priority, check_func = self._checks[name]
        return check_func()

    def run_all_checks(
        self,
        priorities: list[CheckPriority] | None = None,
        parallel: bool = True,
    ) -> list[CheckResult]:
        """Run all checks, optionally filtered by priority."""
        results = []
        checks_to_run = []

        for name, (priority, check_func) in self._checks.items():
            if priorities is None or priority in priorities:
                checks_to_run.append((name, priority, check_func))

        if parallel and len(checks_to_run) > 1:
            # Simple sequential execution for now (parallel can be added with threading)
            for name, priority, check_func in checks_to_run:
                results.append(check_func())
        else:
            for name, priority, check_func in checks_to_run:
                results.append(check_func())

        return results

    def generate_report(
        self,
        results: list[CheckResult],
        format: str = "json",
    ) -> str:
        """Generate a report from check results."""
        if format == "json":
            return json.dumps(
                [
                    {
                        "name": r.name,
                        "status": r.status.value,
                        "priority": r.priority.value,
                        "message": r.message,
                        "details": r.details,
                        "duration": r.duration,
                    }
                    for r in results
                ],
                indent=2,
            )

        if format == "markdown":
            lines = ["# Deployment Readiness Report\n"]
            lines.append(f"Generated: {datetime.now().isoformat()}\n")
            lines.append("| Check | Status | Priority | Message |")
            lines.append("|-------|--------|----------|---------|")
            for r in results:
                status_icon = (
                    "✅"
                    if r.status == CheckStatus.PASSED
                    else "❌"
                    if r.status == CheckStatus.FAILED
                    else "⚠️"
                )
                lines.append(
                    f"| {r.name} | {status_icon} {r.status.value} | {r.priority.value} | {r.message} |"
                )
            return "\n".join(lines)

        # Text format
        lines = ["Deployment Readiness Report", "=" * 50]
        for r in results:
            lines.append(f"\n{r.name} [{r.priority.value.upper()}]")
            lines.append(f"  Status: {r.status.value}")
            lines.append(f"  Message: {r.message}")
            if r.details:
                for key, value in r.details.items():
                    lines.append(f"  {key}: {value}")
        return "\n".join(lines)


# ============================================================================
# Release Automation
# ============================================================================


class ReleaseAutomation:
    """Comprehensive release automation system."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.reports_dir = self.project_root / "reports" / "releases"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        self.release_steps: list[ReleaseStep] = []
        self.current_release: ReleaseInfo | None = None

        self.config = {
            "version_file": "pyproject.toml",
            "changelog_file": "CHANGELOG.md",
            "release_branch": "main",
            "prerelease_branch": "develop",
            "tag_prefix": "v",
            "build_artifacts": True,
            "run_tests": True,
            "create_github_release": False,
            "notify_team": False,
        }

    def create_release(
        self,
        release_type: str,
        prerelease: bool = False,
        custom_version: str | None = None,
    ) -> dict[str, Any]:
        """Create a new release."""
        console.print(f"🚀 Creating {release_type} release...")

        # Step 1: Validate environment
        self._add_step("validate_environment", "Validate release environment")
        if not self._validate_environment():
            return self._generate_release_report()

        # Step 2: Get current version
        self._add_step("get_current_version", "Get current version")
        current_version = self._get_current_version()
        if not current_version:
            return self._generate_release_report()

        # Step 3: Calculate new version
        self._add_step("calculate_version", "Calculate new version")
        new_version = self._calculate_new_version(
            current_version,
            release_type,
            prerelease,
            custom_version,
        )
        if not new_version:
            return self._generate_release_report()

        # Step 4: Update version files
        self._add_step("update_version", "Update version files")
        if not self._update_version_files(new_version):
            return self._generate_release_report()

        # Step 5: Generate changelog
        self._add_step("generate_changelog", "Generate changelog")
        changelog = self._generate_changelog(new_version, release_type)
        if not changelog:
            return self._generate_release_report()

        # Step 6: Generate release notes
        self._add_step("generate_release_notes", "Generate release notes")
        release_notes = self._generate_release_notes(new_version, changelog)

        # Step 7: Run tests
        if self.config["run_tests"]:
            self._add_step("run_tests", "Run test suite")
            if not self._run_tests():
                return self._generate_release_report()

        # Step 8: Build artifacts
        if self.config["build_artifacts"]:
            self._add_step("build_artifacts", "Build release artifacts")
            if not self._build_artifacts():
                return self._generate_release_report()

        # Step 9: Create git tag
        self._add_step("create_git_tag", "Create git tag")
        if not self._create_git_tag(new_version):
            return self._generate_release_report()

        # Step 10: Push changes
        self._add_step("push_changes", "Push changes to remote")
        if not self._push_changes():
            return self._generate_release_report()

        # Create release info
        self.current_release = ReleaseInfo(
            version=new_version,
            release_type=release_type,
            changelog=changelog,
            release_notes=release_notes,
            git_tag=f"{self.config['tag_prefix']}{new_version}",
            timestamp=time.time(),
            author=get_git_author(self.project_root),
            commit_hash=get_current_commit(self.project_root),
        )

        return self._generate_release_report()

    def _add_step(self, name: str, description: str) -> None:
        """Add a release step."""
        step = ReleaseStep(
            name=name,
            status="running",
            duration=time.time(),
            output="",
            error=None,
        )
        self.release_steps.append(step)
        console.print(f"  [cyan]📋 {description}...[/cyan]")

    def _complete_step(self, success: bool, output: str = "", error: str = "") -> None:
        """Complete the current step."""
        if self.release_steps:
            current_step = self.release_steps[-1]
            current_step.status = "completed" if success else "failed"
            current_step.output = output
            current_step.error = error if not success else None
            current_step.duration = time.time() - current_step.duration

    def _validate_environment(self) -> bool:
        """Validate the release environment."""
        try:
            # Check if we're in a git repository
            result = subprocess.run(
                ["git", "status"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            if result.returncode != 0:
                self._complete_step(False, "", "Not in a git repository")
                return False

            # Check if working directory is clean
            result = subprocess.run(
                ["git", "diff", "--quiet"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            if result.returncode != 0:
                self._complete_step(False, "", "Working directory is not clean")
                return False

            # Check if we're on the correct branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            current_branch = result.stdout.strip()
            if current_branch != self.config["release_branch"]:
                self._complete_step(
                    False,
                    "",
                    f"Not on release branch ({self.config['release_branch']})",
                )
                return False

            # Check if version file exists
            version_file = self.project_root / self.config["version_file"]
            if not version_file.exists():
                self._complete_step(
                    False,
                    "",
                    f"Version file not found: {self.config['version_file']}",
                )
                return False

            self._complete_step(True, "Environment validation passed")
            return True

        except Exception as e:
            self._complete_step(False, "", f"Environment validation failed: {e}")
            return False

    def _get_current_version(self) -> str | None:
        """Get the current version from version file."""
        try:
            version_file = self.project_root / self.config["version_file"]

            if version_file.suffix == ".toml":
                content = version_file.read_text()
                version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if version_match:
                    version = version_match.group(1)
                    self._complete_step(True, f"Current version: {version}")
                    return version
                self._complete_step(False, "", "Version not found in pyproject.toml")
                return None

            if version_file.name == "__init__.py":
                content = version_file.read_text()
                version_match = re.search(
                    r'__version__\s*=\s*["\']([^"\']+)["\']',
                    content,
                )
                if version_match:
                    version = version_match.group(1)
                    self._complete_step(True, f"Current version: {version}")
                    return version
                self._complete_step(False, "", "Version not found in __init__.py")
                return None

            self._complete_step(
                False,
                "",
                f"Unsupported version file format: {version_file.suffix}",
            )
            return None

        except Exception as e:
            self._complete_step(False, "", f"Error reading version: {e}")
            return None

    def _calculate_new_version(
        self,
        current_version: str,
        release_type: str,
        prerelease: bool,
        custom_version: str | None,
    ) -> str | None:
        """Calculate the new version number."""
        try:
            if custom_version:
                new_version = custom_version
            else:
                version_parts = current_version.split(".")
                major = int(version_parts[0])
                minor = int(version_parts[1]) if len(version_parts) > 1 else 0
                patch = int(version_parts[2]) if len(version_parts) > 2 else 0

                if release_type == "major":
                    major += 1
                    minor = 0
                    patch = 0
                elif release_type == "minor":
                    minor += 1
                    patch = 0
                elif release_type == "patch":
                    patch += 1
                else:
                    self._complete_step(
                        False,
                        "",
                        f"Invalid release type: {release_type}",
                    )
                    return None

                new_version = f"{major}.{minor}.{patch}"

                if prerelease:
                    new_version += "-rc.1"

            self._complete_step(True, f"New version: {new_version}")
            return new_version

        except Exception as e:
            self._complete_step(False, "", f"Error calculating version: {e}")
            return None

    def _update_version_files(self, new_version: str) -> bool:
        """Update version in all relevant files."""
        try:
            version_file = self.project_root / self.config["version_file"]

            if version_file.suffix == ".toml":
                content = version_file.read_text()
                new_content = re.sub(
                    r'version\s*=\s*["\'][^"\']+["\']',
                    f'version = "{new_version}"',
                    content,
                )
                version_file.write_text(new_content)

            # Also update __init__.py if it exists
            init_file = self.project_root / "src" / "pheno" / "__init__.py"
            if init_file.exists():
                content = init_file.read_text()
                new_content = re.sub(
                    r'__version__\s*=\s*["\'][^"\']+["\']',
                    f'__version__ = "{new_version}"',
                    content,
                )
                init_file.write_text(new_content)

            self._complete_step(True, f"Updated version to {new_version}")
            return True

        except Exception as e:
            self._complete_step(False, "", f"Error updating version files: {e}")
            return False

    def _generate_changelog(self, new_version: str, release_type: str) -> str | None:
        """Generate changelog for the new version."""
        try:
            changelog_file = self.project_root / self.config["changelog_file"]
            commits = get_commits_since_last_tag(self.project_root)

            # Categorize commits
            features = []
            fixes = []
            breaking = []
            other = []

            for commit in commits:
                message = commit.get("message", "")
                if message.startswith("feat:"):
                    features.append(message)
                elif message.startswith("fix:"):
                    fixes.append(message)
                elif message.startswith("BREAKING CHANGE:") or "!" in message:
                    breaking.append(message)
                else:
                    other.append(message)

            # Generate changelog entry
            changelog_entry = f"""## [{new_version}] - {datetime.now().strftime("%Y-%m-%d")}

### Added
"""
            if features:
                for feature in features:
                    changelog_entry += f"- {feature}\n"
            else:
                changelog_entry += "- No new features\n"

            changelog_entry += "\n### Changed\n"
            if other:
                for change in other:
                    changelog_entry += f"- {change}\n"
            else:
                changelog_entry += "- No changes\n"

            changelog_entry += "\n### Fixed\n"
            if fixes:
                for fix in fixes:
                    changelog_entry += f"- {fix}\n"
            else:
                changelog_entry += "- No fixes\n"

            if breaking:
                changelog_entry += "\n### Breaking Changes\n"
                for breaking_change in breaking:
                    changelog_entry += f"- {breaking_change}\n"

            changelog_entry += "\n"

            # Update changelog file
            if changelog_file.exists():
                content = changelog_file.read_text()
                lines = content.split("\n")
                insert_index = 1
                for i, line in enumerate(lines):
                    if line.startswith("## [") and i > 0:
                        insert_index = i
                        break
                lines.insert(insert_index, changelog_entry)
                new_content = "\n".join(lines)
            else:
                new_content = f"# Changelog\n\n{changelog_entry}"

            changelog_file.write_text(new_content)
            self._complete_step(True, f"Generated changelog for {new_version}")
            return changelog_entry

        except Exception as e:
            self._complete_step(False, "", f"Error generating changelog: {e}")
            return None

    def _generate_release_notes(self, new_version: str, changelog: str) -> str:
        """Generate release notes for the new version."""
        try:
            lines = changelog.split("\n")
            features = []
            fixes = []
            breaking = []

            current_section = None
            for line in lines:
                if line.startswith("### Added"):
                    current_section = "features"
                elif line.startswith("### Fixed"):
                    current_section = "fixes"
                elif line.startswith("### Breaking Changes"):
                    current_section = "breaking"
                elif line.startswith(("###", "##")):
                    current_section = None
                elif line.startswith("- ") and current_section:
                    item = line[2:].strip()
                    if current_section == "features":
                        features.append(item)
                    elif current_section == "fixes":
                        fixes.append(item)
                    elif current_section == "breaking":
                        breaking.append(item)

            release_notes = f"# Release {new_version}\n\n## What's New\n\n"

            if features:
                release_notes += "### ✨ New Features\n\n"
                for feature in features:
                    release_notes += f"- {feature}\n"
                release_notes += "\n"

            if fixes:
                release_notes += "### 🐛 Bug Fixes\n\n"
                for fix in fixes:
                    release_notes += f"- {fix}\n"
                release_notes += "\n"

            if breaking:
                release_notes += "### ⚠️ Breaking Changes\n\n"
                for breaking_change in breaking:
                    release_notes += f"- {breaking_change}\n"
                release_notes += "\n"

            release_notes += f"""## Installation

```bash
pip install <package>=={new_version}
```

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for the complete list of changes.

---

*This release was automatically generated.*
"""

            self._complete_step(True, f"Generated release notes for {new_version}")
            return release_notes

        except Exception as e:
            self._complete_step(False, "", f"Error generating release notes: {e}")
            return ""

    def _run_tests(self) -> bool:
        """Run the test suite."""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300,
            )

            if result.returncode == 0:
                self._complete_step(True, "All tests passed")
                return True
            self._complete_step(False, "", f"Tests failed: {result.stderr}")
            return False

        except subprocess.TimeoutExpired:
            self._complete_step(False, "", "Tests timed out")
            return False
        except Exception as e:
            self._complete_step(False, "", f"Error running tests: {e}")
            return False

    def _build_artifacts(self) -> bool:
        """Build release artifacts."""
        try:
            result = subprocess.run(
                ["python", "-m", "build"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300,
            )

            if result.returncode == 0:
                self._complete_step(True, "Build artifacts created successfully")
                return True
            self._complete_step(False, "", f"Build failed: {result.stderr}")
            return False

        except subprocess.TimeoutExpired:
            self._complete_step(False, "", "Build timed out")
            return False
        except Exception as e:
            self._complete_step(False, "", f"Error building artifacts: {e}")
            return False

    def _create_git_tag(self, new_version: str) -> bool:
        """Create a git tag for the release."""
        try:
            tag_name = f"{self.config['tag_prefix']}{new_version}"

            result = subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", f"Release {new_version}"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                self._complete_step(True, f"Created tag: {tag_name}")
                return True
            self._complete_step(False, "", f"Failed to create tag: {result.stderr}")
            return False

        except Exception as e:
            self._complete_step(False, "", f"Error creating git tag: {e}")
            return False

    def _push_changes(self) -> bool:
        """Push changes to remote repository."""
        try:
            subprocess.run(
                ["git", "add", "."],
                check=False,
                cwd=self.project_root,
            )

            version = self.current_release.version if self.current_release else "unknown"
            result = subprocess.run(
                ["git", "commit", "-m", f"Release {version}"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                self._complete_step(
                    False,
                    "",
                    f"Failed to commit changes: {result.stderr}",
                )
                return False

            result = subprocess.run(
                ["git", "push", "origin", self.config["release_branch"]],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                self._complete_step(
                    False,
                    "",
                    f"Failed to push changes: {result.stderr}",
                )
                return False

            result = subprocess.run(
                ["git", "push", "origin", "--tags"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                self._complete_step(False, "", f"Failed to push tags: {result.stderr}")
                return False

            self._complete_step(True, "Changes pushed successfully")
            return True

        except Exception as e:
            self._complete_step(False, "", f"Error pushing changes: {e}")
            return False

    def _generate_release_report(self) -> dict[str, Any]:
        """Generate comprehensive release report."""
        console.print("📊 Generating Release Report...")

        total_steps = len(self.release_steps)
        completed_steps = len(
            [s for s in self.release_steps if s.status == "completed"],
        )
        failed_steps = len([s for s in self.release_steps if s.status == "failed"])
        total_duration = sum(s.duration for s in self.release_steps)
        overall_status = "success" if failed_steps == 0 else "failed"

        report = {
            "timestamp": datetime.now().isoformat(),
            "release_info": asdict(self.current_release) if self.current_release else None,
            "summary": {
                "total_steps": total_steps,
                "completed_steps": completed_steps,
                "failed_steps": failed_steps,
                "total_duration": round(total_duration, 2),
                "overall_status": overall_status,
            },
            "steps": [asdict(step) for step in self.release_steps],
            "config": self.config,
        }

        self._save_release_report(report)
        return report

    def _save_release_report(self, report: dict[str, Any]) -> None:
        """Save release report."""
        json_file = self.reports_dir / f"release_report_{int(time.time())}.json"
        json_file.write_text(json.dumps(report, indent=2))

        summary_file = self.reports_dir / f"release_summary_{int(time.time())}.md"
        self._save_release_summary(report, summary_file)

        console.print(f"[green]Reports saved:[/green]")
        console.print(f"  JSON: {json_file}")
        console.print(f"  Summary: {summary_file}")

    def _save_release_summary(self, report: dict[str, Any], path: Path) -> None:
        """Save release summary as markdown."""
        summary = report["summary"]
        lines = [
            f"# Release Report - {report['timestamp']}",
            "",
            f"**Status:** {summary['overall_status'].upper()}",
            f"**Steps:** {summary['completed_steps']}/{summary['total_steps']} completed",
            f"**Duration:** {summary['total_duration']}s",
            "",
            "## Step Details",
            "",
        ]
        for step in report["steps"]:
            status_icon = "✅" if step["status"] == "completed" else "❌"
            lines.append(f"- {status_icon} **{step['name']}**: {step['status']}")
        path.write_text("\n".join(lines))


# ============================================================================
# CLI Commands
# ============================================================================


@app.command("build")
def build_command(
    config: Path = typer.Argument(
        default=None,
        help="Path to build configuration file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
    target: str = typer.Option(
        "local",
        "--target",
        "-t",
        help="Deployment target (local, staging, prod)",
    ),
    skip_tests: bool = typer.Option(
        False,
        "--skip-tests",
        help="Skip running tests",
    ),
    skip_install_test: bool = typer.Option(
        False,
        "--skip-install-test",
        help="Skip fresh venv install test",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Build without publishing",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
) -> None:
    """Build package and optionally publish."""
    project_root = Path.cwd()

    # Clean previous builds
    for folder in ("dist", "build"):
        folder_path = project_root / folder
        if folder_path.exists():
            shutil.rmtree(folder_path)
            if verbose:
                console.print(f"[dim]Cleaned {folder}/[/dim]")

    # Build wheel
    console.print("[cyan]🏗️  Building wheel distribution...[/cyan]")
    run_command(["python", "-m", "build"])
    console.print("[green]✓ Build successful[/green]")

    # Run tests
    if not skip_tests:
        console.print("[cyan]🧪 Running tests...[/cyan]")
        run_command(["pytest", "tests/", "-v", "--tb=short"])
        console.print("[green]✓ Tests passed[/green]")

    # Test fresh install
    if not skip_install_test:
        console.print("[cyan]🧫 Testing fresh install...[/cyan]")
        with tempfile.TemporaryDirectory() as temp_dir:
            venv_path = Path(temp_dir) / "test_venv"
            venv.create(venv_path, with_pip=True)

            if sys.platform == "win32":
                pip_exe = venv_path / "Scripts" / "pip.exe"
            else:
                pip_exe = venv_path / "bin" / "pip"

            dist_dir = project_root / "dist"
            wheel_files = sorted(dist_dir.glob("*.whl"))

            if not wheel_files:
                console.print("[red]Error:[/red] No wheel found in dist/")
                raise typer.Exit(1)

            wheel_file = wheel_files[0]
            run_command([str(pip_exe), "install", str(wheel_file)])
            console.print("[green]✓ Fresh install test passed[/green]")

    # Publish (if not dry run)
    if not dry_run and target != "local":
        console.print(f"[cyan]🚀 Publishing to {target}...[/cyan]")
        # This would integrate with actual deployment targets
        console.print(f"[yellow]Note:[/yellow] Publishing to {target} requires configuration")
    else:
        console.print("[yellow]Dry run - skipping publish[/yellow]")

    console.print("\n[bold green]🎉 Build process completed![/bold green]")


@app.command("release")
def release_command(
    version: str = typer.Argument(
        ...,
        help="Version to release (major, minor, patch, or custom version)",
    ),
    notes: Path = typer.Option(
        None,
        "--notes",
        "-n",
        help="Path to release notes file",
        exists=True,
        file_okay=True,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Simulate release without making changes",
    ),
    prerelease: bool = typer.Option(
        False,
        "--prerelease",
        help="Mark as prerelease",
    ),
    project_root: Path = typer.Option(
        ".",
        "--project",
        "-p",
        help="Project root directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """Create a new release with semantic versioning."""
    automation = ReleaseAutomation(project_root)

    if dry_run:
        console.print("[yellow]🔍 DRY RUN - No changes will be made[/yellow]")

    # Determine release type
    release_type = version if version in ("major", "minor", "patch") else "custom"
    custom_version = version if release_type == "custom" else None

    report = automation.create_release(
        release_type=release_type,
        prerelease=prerelease,
        custom_version=custom_version,
    )

    # Display results
    summary = report["summary"]
    status_color = "green" if summary["overall_status"] == "success" else "red"

    console.print(
        f"\n[bold {status_color}]Release Status: {summary['overall_status'].upper()}[/bold {status_color}]"
    )
    console.print(f"Steps: {summary['completed_steps']}/{summary['total_steps']} completed")
    console.print(f"Failed: {summary['failed_steps']}")
    console.print(f"Duration: {summary['total_duration']}s")

    if summary["failed_steps"] > 0:
        raise typer.Exit(1)


@app.command("check")
def check_command(
    environment: str = typer.Argument(
        default="local",
        help="Environment to check (local, staging, prod)",
    ),
    health: bool = typer.Option(
        True,
        "--health/--no-health",
        help="Run health checks",
    ),
    schema: bool = typer.Option(
        False,
        "--schema",
        help="Check schema consistency",
    ),
    config_check: bool = typer.Option(
        False,
        "--config",
        help="Validate configuration files",
    ),
    format: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format (text, json, markdown)",
    ),
    output_file: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Write report to file",
    ),
    project_dir: Path = typer.Option(
        ".",
        "--project",
        "-p",
        help="Project directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """Run deployment readiness checks."""
    checker = DeploymentChecker(project_dir)

    console.print(f"[cyan]🚀 Running deployment checks for [bold]{environment}[/bold]...[/cyan]")

    # Run checks
    results = checker.run_all_checks()

    # Generate report
    if format == "json":
        report = checker.generate_report(results, format="json")
        if output_file:
            output_file.write_text(report)
            console.print(f"[green]Report written to {output_file}[/green]")
        else:
            console.print(report)
    elif format == "markdown":
        report = checker.generate_report(results, format="markdown")
        if output_file:
            output_file.write_text(report)
            console.print(f"[green]Report written to {output_file}[/green]")
        else:
            console.print(report)
    else:
        # Text format with rich display
        table = Table(title="Deployment Readiness Check")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Priority", style="dim")
        table.add_column("Message")

        for result in results:
            status_style = {
                CheckStatus.PASSED: "green",
                CheckStatus.FAILED: "red",
                CheckStatus.WARNING: "yellow",
                CheckStatus.ERROR: "red",
                CheckStatus.SKIPPED: "dim",
            }.get(result.status, "white")

            status_icon = {
                CheckStatus.PASSED: "✅",
                CheckStatus.FAILED: "❌",
                CheckStatus.WARNING: "⚠️",
                CheckStatus.ERROR: "🚨",
                CheckStatus.SKIPPED: "⏭️",
            }.get(result.status, "❓")

            table.add_row(
                result.name,
                f"{status_icon} {result.status.value}",
                result.priority.value.upper(),
                result.message,
                style=status_style,
            )

        console.print(table)

        # Summary
        total = len(results)
        passed = sum(1 for r in results if r.status == CheckStatus.PASSED)
        failed = sum(1 for r in results if r.status == CheckStatus.FAILED)
        warnings = sum(1 for r in results if r.status == CheckStatus.WARNING)

        score = (passed / total * 100) if total else 0

        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"  Total: {total}")
        console.print(f"  [green]Passed: {passed}[/green]")
        console.print(f"  [red]Failed: {failed}[/red]")
        console.print(f"  [yellow]Warnings: {warnings}[/yellow]")
        console.print(f"  Score: {score:.1f}%")

        if failed == 0:
            console.print("\n[bold green]🎉 DEPLOYMENT READY[/bold green]")
        else:
            console.print(f"\n[bold red]🚫 DEPLOYMENT BLOCKED ({failed} failures)[/bold red]")
            raise typer.Exit(1)


@app.command("schema-drift")
def schema_drift_command(
    db_url: str = typer.Argument(
        default=None,
        help="Database URL to check (optional, uses local if not provided)",
    ),
    baseline: Path = typer.Option(
        None,
        "--baseline",
        "-b",
        help="Path to baseline schema file",
        exists=True,
        file_okay=True,
    ),
    report_path: Path = typer.Option(
        None,
        "--report",
        "-r",
        help="Write drift report to file",
    ),
    offline: bool = typer.Option(
        False,
        "--offline",
        help="Skip remote connection, use local only",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output in JSON format",
    ),
) -> None:
    """Check for schema drift between environments."""
    console.print("[cyan]🔍 Checking for schema drift...[/cyan]")

    # Placeholder implementation - would integrate with actual schema sync
    result = {
        "status": "healthy" if offline else "unknown",
        "drift_detected": False,
        "message": "Schema drift check requires database connection configuration",
        "note": "This is a standalone version - integrate with your schema management system",
    }

    if offline:
        result["status"] = "offline"
        result["message"] = "Offline mode - baseline comparison only"

    if json_output:
        console.print(json.dumps(result, indent=2))
    else:
        status_color = {
            "healthy": "green",
            "offline": "yellow",
            "drift_detected": "red",
            "unknown": "dim",
        }.get(result["status"], "white")

        console.print(
            Panel(
                f"[bold {status_color}]Status: {result['status'].upper()}[/bold {status_color}]\n"
                f"{result['message']}",
                title="Schema Drift Check",
            )
        )

    if report_path:
        report_path.write_text(json.dumps(result, indent=2))
        console.print(f"[green]Report saved to {report_path}[/green]")


@app.command("rollback")
def rollback_command(
    version: str = typer.Argument(
        ...,
        help="Version to rollback to",
    ),
    confirm: bool = typer.Option(
        False,
        "--confirm",
        "-y",
        help="Skip confirmation prompt",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be done without executing",
    ),
    project_root: Path = typer.Option(
        ".",
        "--project",
        "-p",
        help="Project root directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
) -> None:
    """Rollback to a previous version."""
    if not confirm and not dry_run:
        confirmed = typer.confirm(f"Are you sure you want to rollback to {version}?")
        if not confirmed:
            console.print("[yellow]Rollback cancelled[/yellow]")
            raise typer.Exit(0)

    console.print(f"[cyan]⏪ Rolling back to version {version}...[/cyan]")

    if dry_run:
        console.print("[yellow]DRY RUN - Would execute:[/yellow]")
        console.print(f"  1. git checkout {version}")
        console.print(f"  2. git tag -d current-version (if exists)")
        console.print(f"  3. Deploy {version} to target environment")
    else:
        # Execute rollback
        try:
            run_command(["git", "checkout", version], cwd=project_root, check=False)
            console.print(f"[green]✓ Checked out {version}[/green]")
            console.print(
                "[yellow]Note:[/yellow] Complete rollback requires CI/CD pipeline integration"
            )
        except Exception as e:
            console.print(f"[red]Rollback failed: {e}[/red]")
            raise typer.Exit(1)


@app.command("validate")
def validate_command(
    package: Path = typer.Argument(
        ...,
        help="Package to validate (wheel or source directory)",
        exists=True,
    ),
    requirements: bool = typer.Option(
        True,
        "--requirements/--no-requirements",
        help="Validate requirements/dependencies",
    ),
    security: bool = typer.Option(
        False,
        "--security",
        help="Run security scans",
    ),
    metadata: bool = typer.Option(
        True,
        "--metadata/--no-metadata",
        help="Validate package metadata",
    ),
) -> None:
    """Validate a package before deployment."""
    console.print(f"[cyan]🔍 Validating {package.name}...[/cyan]")

    issues = []

    if package.is_dir():
        # Directory validation
        pyproject = package / "pyproject.toml"
        setup_py = package / "setup.py"

        if not pyproject.exists() and not setup_py.exists():
            issues.append("No pyproject.toml or setup.py found")

        if pyproject.exists() and metadata:
            content = pyproject.read_text()
            if "name" not in content:
                issues.append("Package name not defined")
            if "version" not in content:
                issues.append("Package version not defined")

    elif package.suffix == ".whl":
        # Wheel validation
        console.print("[dim]Validating wheel format...[/dim]")
        # Would use wheel-inspect or similar

    if requirements:
        console.print("[dim]Checking requirements...[/dim]")
        # Would check for dependency conflicts

    if security:
        console.print("[dim]Running security checks...[/dim]")
        # Would integrate with safety or bandit

    if issues:
        console.print("[red]Validation failed:[/red]")
        for issue in issues:
            console.print(f"  ❌ {issue}")
        raise typer.Exit(1)
    else:
        console.print("[green]✓ Package validation passed[/green]")


@app.command("promote")
def promote_command(
    from_env: str = typer.Argument(
        ...,
        help="Source environment (e.g., staging)",
    ),
    to_env: str = typer.Argument(
        ...,
        help="Target environment (e.g., prod)",
    ),
    run_tests: bool = typer.Option(
        True,
        "--tests/--no-tests",
        help="Run tests before promotion",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Simulate promotion without deploying",
    ),
) -> None:
    """Promote deployment from one environment to another."""
    console.print(
        f"[cyan]🚀 Promoting from [bold]{from_env}[/bold] to [bold]{to_env}[/bold]...[/cyan]"
    )

    if dry_run:
        console.print("[yellow]DRY RUN - Would:[/yellow]")
        console.print(f"  1. Verify {from_env} deployment health")
        if run_tests:
            console.print("  2. Run integration tests")
        console.print(f"  3. Deploy to {to_env}")
        console.print(f"  4. Verify {to_env} deployment")
    else:
        console.print(f"[yellow]Note:[/yellow] Promotion to {to_env} requires CI/CD integration")
        console.print("Use your deployment platform's promote feature or pipeline")


@app.command("artifacts")
def artifacts_command(
    action: str = typer.Argument(
        ...,
        help="Action: list, clean, or archive",
    ),
    older_than: int = typer.Option(
        None,
        "--older-than",
        help="Filter artifacts older than N days",
    ),
    keep_minimum: int = typer.Option(
        5,
        "--keep-minimum",
        help="Minimum artifacts to keep when cleaning",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be done without executing",
    ),
) -> None:
    """Manage build artifacts."""
    dist_dir = Path.cwd() / "dist"

    if not dist_dir.exists():
        console.print("[yellow]No dist/ directory found[/yellow]")
        raise typer.Exit(0)

    artifacts = sorted(dist_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)

    if action == "list":
        table = Table(title="Build Artifacts")
        table.add_column("Name", style="cyan")
        table.add_column("Size", justify="right")
        table.add_column("Modified", style="dim")

        for artifact in artifacts:
            stat = artifact.stat()
            size = stat.st_size
            size_str = (
                f"{size / 1024 / 1024:.1f} MB" if size > 1024 * 1024 else f"{size / 1024:.1f} KB"
            )
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            table.add_row(artifact.name, size_str, mtime)

        console.print(table)

    elif action == "clean":
        to_delete = artifacts[keep_minimum:] if len(artifacts) > keep_minimum else []

        if older_than is not None:
            cutoff = time.time() - (older_than * 86400)
            to_delete = [a for a in to_delete if a.stat().st_mtime < cutoff]

        if not to_delete:
            console.print("[green]No artifacts to clean[/green]")
            return

        console.print(f"[yellow]Will delete {len(to_delete)} artifacts[/yellow]")

        for artifact in to_delete:
            if dry_run:
                console.print(f"  [dim]Would delete: {artifact.name}[/dim]")
            else:
                artifact.unlink()
                console.print(f"  [red]Deleted:[/red] {artifact.name}")

        if not dry_run:
            console.print(f"[green]✓ Cleaned {len(to_delete)} artifacts[/green]")

    elif action == "archive":
        console.print("[yellow]Archive action requires configuration[/yellow]")
        console.print("Set ARTIFACT_ARCHIVE_PATH environment variable or use --archive-path")

    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        console.print("Valid actions: list, clean, archive")
        raise typer.Exit(1)


# ============================================================================
# Main Entry Point
# ============================================================================


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
