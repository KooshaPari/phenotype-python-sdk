"""Health check primitives: statuses, check results, checkers, and a monitor."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class HealthStatus(str, Enum):
    """Overall health status values."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Result of a single health check."""

    name: str
    status: HealthStatus
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    response_time: float = 0.0


@dataclass
class HealthConfig:
    """Configuration for health monitoring."""

    check_interval: float = 30.0
    timeout: float = 5.0
    retry_count: int = 3
    enable_monitoring: bool = True


class HealthChecker(ABC):
    """Abstract base class for individual health checkers."""

    @abstractmethod
    async def check_health(self) -> HealthCheck:
        """Run the health check and return its result."""
        raise NotImplementedError


class HealthMonitor:
    """Aggregates registered checkers into per-name results and overall status."""

    def __init__(self, config: HealthConfig | None = None) -> None:
        self.config = config or HealthConfig()
        self._checkers: dict[str, HealthChecker] = {}

    def add_checker(self, name: str, checker: HealthChecker) -> None:
        """Register a checker under ``name``."""
        self._checkers[name] = checker

    def remove_checker(self, name: str) -> bool:
        """Remove a checker; return True when it existed."""
        return self._checkers.pop(name, None) is not None

    async def check_all(self) -> dict[str, HealthCheck]:
        """Run all registered checkers and return results keyed by name."""
        results: dict[str, HealthCheck] = {}
        for name, checker in self._checkers.items():
            results[name] = await checker.check_health()
        return results

    async def get_overall_health(self) -> HealthStatus:
        """Derive overall status: any unhealthy wins, then any degraded."""
        results = await self.check_all()
        if not results:
            return HealthStatus.UNKNOWN
        statuses = {check.status for check in results.values()}
        if HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY
        if HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY
