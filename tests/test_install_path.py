"""Regression tests for upstream packaging flat-layout defect.

Background
----------

The consolidated workspace root has ``okf/`` and ``packages/`` as
top-level directories, so external consumers running
``uv pip install <workspace-path>`` or ``pip install <workspace-path>``
on the upstream repo used to fail with::

    error: Multiple top-level packages discovered in a flat-layout:
    ['okf', 'packages']

because setuptools' default auto-discovery conflicted on those two
directories. The root project is a uv workspace aggregator only (no
installable Python module of its own), so ``[tool.uv] package = false``
stops implicit uv builds, but explicit installs ignore that flag.

These tests pin the desired end-state: the workspace must be installable
as a path source (no flat-layout error, exit 0) in a fresh venv.

Traces to: AUDIT-LANE-FLAT-LAYOUT-001 (Phenotype-python-sdk packaging
audit, second lane after PR #42 ``fix/auth-kit-gitlink``).
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"

# A venv creation on macOS routinely takes ~1.5s and pip install ~2.5s,
# so give the subprocess a generous budget for CI runners.
_INSTALL_TIMEOUT_SECS = 120


def _uv_available() -> bool:
    return shutil.which("uv") is not None


def _create_temp_venv(python_version: str = "3.13") -> tuple[Path, Path]:
    """Create an ephemeral Python venv at *tempdir/.venv* via uv.

    Returns ``(tempdir, venv_python)``. The caller is responsible for
    cleaning up *tempdir* via :func:`_cleanup_temp_venv`.
    """
    tempdir = Path(tempfile.mkdtemp(prefix="phenotype-sdk-install-"))
    venv_dir = tempdir / ".venv"
    proc = subprocess.run(
        (
            "uv",
            "venv",
            "--python",
            python_version,
            str(venv_dir),
        ),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"uv venv creation failed (rc={proc.returncode}):\n"
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
    return tempdir, venv_dir


def _cleanup_temp_venv(tempdir: Path) -> None:
    """Best-effort teardown of a temp venv directory tree."""
    if not tempdir.exists():
        return
    shutil.rmtree(tempdir, ignore_errors=True)


def _run_uv_pip_install(
    venv_python: Path,
    extra_args: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    """Run ``uv pip install <args> <repo-path>`` against the venv."""
    cmd = [
        "uv",
        "pip",
        "install",
        "--python",
        str(venv_python),
        *extra_args,
        str(REPO_ROOT),
    ]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=_INSTALL_TIMEOUT_SECS,
    )


# Skip the entire module if uv is missing — this is an upstream packaging
# regression, the test is meaningless without uv available.
pytestmark = pytest.mark.skipif(
    not _uv_available(),
    reason="uv CLI not available on PATH; install uv to run packaging tests",
)


@pytest.fixture
def temp_venv():
    """Yield ``(tempdir, venv_python)`` for one test, cleanup on exit."""
    tempdir, venv_dir = _create_temp_venv("3.13")
    venv_python = venv_dir / "bin" / "python"
    try:
        yield tempdir, venv_python
    finally:
        _cleanup_temp_venv(tempdir)


def test_workspace_installs_as_path_source(temp_venv) -> None:
    """``uv pip install <repo>`` completes with exit 0 in a fresh venv.

    Regression: previously failed with ``Multiple top-level packages
    discovered in a flat-layout: ['okf', 'packages']``.
    """
    _, venv_python = temp_venv
    result = _run_uv_pip_install(venv_python)

    assert result.returncode == 0, (
        f"uv pip install failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )


def test_workspace_install_does_not_emit_flat_layout_error(temp_venv) -> None:
    """The flat-layout auto-discovery error string never appears, even
    when the install fails for unrelated reasons."""
    _, venv_python = temp_venv
    result = _run_uv_pip_install(venv_python)

    combined = result.stdout + "\n" + result.stderr
    assert "Multiple top-level packages discovered in a flat-layout" not in combined, (
        "flat-layout auto-discovery regressed:\n" + combined
    )
    assert "['okf', 'packages']" not in combined, (
        "flat-layout auto-discovery regressed (conflict list leaked):\n" + combined
    )


def test_workspace_editable_install_succeeds(temp_venv) -> None:
    """``uv pip install -e <repo>`` (editable) also completes cleanly."""
    _, venv_python = temp_venv
    result = _run_uv_pip_install(venv_python, extra_args=("-e",))

    assert result.returncode == 0, (
        f"uv pip install -e failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    assert "Multiple top-level packages" not in (result.stdout + result.stderr), (
        "editable install hit flat-layout error:\n" + result.stderr
    )


def test_pyproject_declares_empty_tool_setuptools() -> None:
    """Pin the chosen fix: ``[tool.setuptools] py-modules = []`` plus a
    no-op ``packages.find`` table that disables auto-discovery."""
    text = PYPROJECT.read_text()
    assert "[tool.setuptools]" in text, (
        "missing [tool.setuptools] section in root pyproject.toml"
    )
    assert "py-modules = []" in text, (
        "[tool.setuptools] should declare py-modules = [] to suppress "
        "flat-layout auto-discovery"
    )
    assert "[tool.setuptools.packages.find]" in text, (
        "missing [tool.setuptools.packages.find] section; cannot pin "
        "no-package discovery for consumers"
    )
