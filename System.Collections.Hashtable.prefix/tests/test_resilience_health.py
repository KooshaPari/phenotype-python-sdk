"""Tests for pheno-resilience health module."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from pheno_resilience.health import (
    HealthCheck,
    HealthChecker,
    HealthConfig,
    HealthMonitor,
    HealthStatus,
)


class TestHealthStatus:
    """Tests for HealthStatus enum."""

    def test_all_statuses_exist(self) -> None:
        """Test all expected health statuses exist."""
        assert HealthStatus.HEALTHY is not None
        assert HealthStatus.DEGRADED is not None
        assert HealthStatus.UNHEALTHY is not None
        assert HealthStatus.UNKNOWN is not None

    def test_status_values(self) -> None:
        """Test health status string values."""
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.DEGRADED.value == "degraded"
        assert HealthStatus.UNHEALTHY.value == "unhealthy"
        assert HealthStatus.UNKNOWN.value == "unknown"


class TestHealthCheck:
    """Tests for HealthCheck dataclass."""

    def test_health_check_basic(self) -> None:
        """Test basic HealthCheck creation."""
        check = HealthCheck(
            name="test_check",
            status=HealthStatus.HEALTHY,
            message="All good",
        )

        assert check.name == "test_check"
        assert check.status == HealthStatus.HEALTHY
        assert check.message == "All good"
        assert check.details == {}
        assert check.timestamp is not None
        assert check.response_time == 0.0

    def test_health_check_with_details(self) -> None:
        """Test HealthCheck with details."""
        details = {"cpu_percent": 45.2, "memory_mb": 512}
        check = HealthCheck(
            name="system_check",
            status=HealthStatus.HEALTHY,
            message="System OK",
            details=details,
            response_time=0.5,
        )

        assert check.details == details
        assert check.response_time == 0.5

    def test_health_check_default_timestamp(self) -> None:
        """Test that timestamp defaults to current time."""
        before = datetime.now()
        check = HealthCheck(name="test", status=HealthStatus.HEALTHY)
        after = datetime.now()

        assert before <= check.timestamp <= after


class TestHealthConfig:
    """Tests for HealthConfig dataclass."""

    def test_config_defaults(self) -> None:
        """Test HealthConfig default values."""
        config = HealthConfig()

        assert config.check_interval == 30.0
        assert config.timeout == 5.0
        assert config.retry_count == 3
        assert config.enable_monitoring is True

    def test_config_custom(self) -> None:
        """Test HealthConfig with custom values."""
        config = HealthConfig(
            check_interval=60.0,
            timeout=10.0,
            retry_count=5,
            enable_monitoring=False,
        )

        assert config.check_interval == 60.0
        assert config.timeout == 10.0
        assert config.retry_count == 5
        assert config.enable_monitoring is False


class TestHealthChecker:
    """Tests for HealthChecker abstract class."""

    def test_health_checker_is_abstract(self) -> None:
        """Test HealthChecker cannot be instantiated directly."""
        with pytest.raises(TypeError):
            HealthChecker()


class MockHealthChecker(HealthChecker):
    """Mock health checker for testing."""

    def __init__(self, result_status: HealthStatus = HealthStatus.HEALTHY):
        self._result_status = result_status

    async def check_health(self) -> HealthCheck:
        return HealthCheck(
            name="mock_checker",
            status=self._result_status,
            message="Mock health check",
        )


class TestHealthMonitor:
    """Tests for HealthMonitor."""

    def test_monitor_initialization(self) -> None:
        """Test HealthMonitor initialization."""
        monitor = HealthMonitor()
        assert monitor.config is not None
        assert len(monitor._checkers) == 0

    def test_monitor_with_custom_config(self) -> None:
        """Test HealthMonitor with custom config."""
        config = HealthConfig(check_interval=10.0, timeout=2.0)
        monitor = HealthMonitor(config=config)

        assert monitor.config.check_interval == 10.0
        assert monitor.config.timeout == 2.0

    def test_add_checker(self) -> None:
        """Test adding a health checker."""
        monitor = HealthMonitor()
        checker = MockHealthChecker()

        monitor.add_checker("test_checker", checker)
        assert "test_checker" in monitor._checkers

    def test_remove_checker_exists(self) -> None:
        """Test removing an existing checker."""
        monitor = HealthMonitor()
        checker = MockHealthChecker()
        monitor.add_checker("test_checker", checker)

        result = monitor.remove_checker("test_checker")
        assert result is True
        assert "test_checker" not in monitor._checkers

    def test_remove_checker_not_exists(self) -> None:
        """Test removing a non-existent checker."""
        monitor = HealthMonitor()

        result = monitor.remove_checker("nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_check_all_no_checkers(self) -> None:
        """Test check_all with no checkers."""
        monitor = HealthMonitor()
        results = await monitor.check_all()

        assert results == {}

    @pytest.mark.asyncio
    async def test_check_all_with_checker(self) -> None:
        """Test check_all with a checker."""
        monitor = HealthMonitor()
        checker = MockHealthChecker(HealthStatus.HEALTHY)
        monitor.add_checker("healthy_check", checker)

        results = await monitor.check_all()

        assert "healthy_check" in results
        assert results["healthy_check"].status == HealthStatus.HEALTHY

    @pytest.mark.asyncio
    async def test_check_all_with_unhealthy_checker(self) -> None:
        """Test check_all with an unhealthy checker."""
        monitor = HealthMonitor()
        checker = MockHealthChecker(HealthStatus.UNHEALTHY)
        monitor.add_checker("unhealthy_check", checker)

        results = await monitor.check_all()

        assert "unhealthy_check" in results
        assert results["unhealthy_check"].status == HealthStatus.UNHEALTHY

    @pytest.mark.asyncio
    async def test_get_overall_health_no_checkers(self) -> None:
        """Test get_overall_health with no checkers."""
        monitor = HealthMonitor()
        status = await monitor.get_overall_health()

        assert status == HealthStatus.UNKNOWN

    @pytest.mark.asyncio
    async def test_get_overall_health_all_healthy(self) -> None:
        """Test get_overall_health when all checks are healthy."""
        monitor = HealthMonitor()
        monitor.add_checker("check1", MockHealthChecker(HealthStatus.HEALTHY))
        monitor.add_checker("check2", MockHealthChecker(HealthStatus.HEALTHY))

        status = await monitor.get_overall_health()
        assert status == HealthStatus.HEALTHY

    @pytest.mark.asyncio
    async def test_get_overall_health_one_unhealthy(self) -> None:
        """Test get_overall_health when one check is unhealthy."""
        monitor = HealthMonitor()
        monitor.add_checker("healthy", MockHealthChecker(HealthStatus.HEALTHY))
        monitor.add_checker("unhealthy", MockHealthChecker(HealthStatus.UNHEALTHY))

        status = await monitor.get_overall_health()
        assert status == HealthStatus.UNHEALTHY

    @pytest.mark.asyncio
    async def test_get_overall_health_degraded(self) -> None:
        """Test get_overall_health when checks are degraded but not unhealthy."""
        monitor = HealthMonitor()
        monitor.add_checker("check1", MockHealthChecker(HealthStatus.HEALTHY))
        monitor.add_checker("check2", MockHealthChecker(HealthStatus.DEGRADED))

        status = await monitor.get_overall_health()
        assert status == HealthStatus.DEGRADED
