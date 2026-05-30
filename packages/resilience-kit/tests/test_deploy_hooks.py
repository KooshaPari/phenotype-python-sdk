"""Tests for deploy-kit hooks module."""

from __future__ import annotations

from pathlib import Path

import pytest

from pheno_deploy_kit.hooks import (
    DeploymentHook,
    HookRegistry,
    PostDeployHook,
    PreDeployHook,
    get_changed_files,
    get_project_root,
    requirements_changed,
)


class TestDeploymentHook:
    """Tests for DeploymentHook base class."""

    def test_deployment_hook_is_abstract(self) -> None:
        """Test DeploymentHook cannot be instantiated directly."""
        with pytest.raises(TypeError):
            DeploymentHook()


class TestPreDeployHook:
    """Tests for PreDeployHook class."""

    def test_pre_deploy_hook_is_deployment_hook(self) -> None:
        """Test PreDeployHook is a DeploymentHook subclass."""
        assert issubclass(PreDeployHook, DeploymentHook)


class TestPostDeployHook:
    """Tests for PostDeployHook class."""

    def test_post_deploy_hook_is_deployment_hook(self) -> None:
        """Test PostDeployHook is a DeploymentHook subclass."""
        assert issubclass(PostDeployHook, DeploymentHook)


class TestHookRegistry:
    """Tests for HookRegistry class."""

    def test_registry_initialization(self) -> None:
        """Test HookRegistry initialization."""
        registry = HookRegistry()

        assert len(registry._hooks) == 0

    def test_register_hook(self) -> None:
        """Test registering a hook."""
        registry = HookRegistry()
        
        class TestHook(DeploymentHook):
            def execute(self, context):
                return True
        
        hook = TestHook()

        registry.register(hook)

        assert len(registry._hooks) == 1
        assert hook in registry._hooks

    def test_execute_all(self) -> None:
        """Test executing all hooks."""
        registry = HookRegistry()

        call_count = {"count": 0}

        class TestHook(DeploymentHook):
            def execute(self, context):
                call_count["count"] += 1
                return True

        hook1 = TestHook()
        hook2 = TestHook()

        registry.register(hook1)
        registry.register(hook2)

        result = registry.execute_all({})

        assert result is True
        assert call_count["count"] == 2


class TestGetProjectRoot:
    """Tests for get_project_root function."""

    def test_get_project_root_returns_path(self) -> None:
        """Test get_project_root returns a Path."""
        root = get_project_root()

        assert isinstance(root, Path)


class TestGetChangedFiles:
    """Tests for get_changed_files function."""

    def test_get_changed_files_returns_list(self) -> None:
        """Test get_changed_files returns a list."""
        files = get_changed_files()

        assert isinstance(files, list)


class TestRequirementsChanged:
    """Tests for requirements_changed function."""

    def test_requirements_changed_true(self) -> None:
        """Test requirements_changed with requirements.txt in list."""
        files = ["src/main.py", "requirements.txt", "README.md"]

        assert requirements_changed(files) is True

    def test_requirements_changed_false(self) -> None:
        """Test requirements_changed without requirements.txt."""
        files = ["src/main.py", "README.md", "tests/test.py"]

        assert requirements_changed(files) is False

    def test_requirements_changed_empty_list(self) -> None:
        """Test requirements_changed with empty list."""
        assert requirements_changed([]) is False

    def test_requirements_changed_none(self) -> None:
        """Test requirements_changed with None (auto-detect)."""
        # Should return False when no changes detected
        result = requirements_changed(None)
        assert isinstance(result, bool)
