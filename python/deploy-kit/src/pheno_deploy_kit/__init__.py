"""
Pheno-Deploy-Kit: Universal deployment abstraction for cloud platforms and local services.

This kit provides unified interfaces for deploying applications across:
- Vercel (serverless, edge functions)
- Fly.io (containers, global distribution)
- Local processes (development, testing)
- Docker (containerization)

Features:
- Platform-agnostic deployment abstractions
- Local service management with process isolation
- Health check patterns (HTTP, TCP, custom probes)
- Build hook generation
- Environment variable management
- NVMS (Node Version Manager Script) parsing
- Package vendoring utilities
- Deployment validation
- Platform detection and configuration
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

# ============================================================================
# Local Health Check Implementations (extracted from pheno.* imports)
# ============================================================================

@dataclass
class HealthCheckResult:
    """Result of a health check execution."""

    healthy: bool
    message: str = ""
    latency_ms: float = 0.0
    metadata: dict[str, Any] | None = None


class HealthCheck(ABC):
    """Abstract base class for health checks."""

    def __init__(self, name: str | None = None, timeout: float = 5.0):
        self.name = name or self.__class__.__name__
        self.timeout = timeout

    @abstractmethod
    async def run(self) -> HealthCheckResult:
        """Execute the health check."""
        ...


class HealthChecker:
    """Manager for multiple health checks."""

    def __init__(self):
        self._checks: list[HealthCheck] = []

    def add_check(self, check: HealthCheck) -> None:
        """Add a health check to the registry."""
        self._checks.append(check)

    async def run_all(self) -> dict[str, HealthCheckResult]:
        """Run all registered health checks."""
        results: dict[str, HealthCheckResult] = {}
        for check in self._checks:
            try:
                results[check.name] = await check.run()
            except Exception as e:
                results[check.name] = HealthCheckResult(
                    healthy=False, message=f"Check failed: {e}"
                )
        return results

    def get_overall_health(self, results: dict[str, HealthCheckResult]) -> bool:
        """Determine overall health from individual results."""
        return all(r.healthy for r in results.values())


class HTTPHealthCheck(HealthCheck):
    """HTTP-based health check."""

    def __init__(
        self,
        url: str,
        expected_status: int = 200,
        timeout: float = 5.0,
        name: str | None = None,
    ):
        super().__init__(name=name or f"http_{url}", timeout=timeout)
        self.url = url
        self.expected_status = expected_status

    async def run(self) -> HealthCheckResult:
        """Execute HTTP health check."""
        import asyncio
        import time

        start = time.time()
        try:
            # Simple HTTP check using asyncio
            import urllib.request

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: urllib.request.urlopen(self.url, timeout=self.timeout)
            )
            status = response.getcode()
            latency = (time.time() - start) * 1000

            if status == self.expected_status:
                return HealthCheckResult(
                    healthy=True,
                    message=f"HTTP {status}",
                    latency_ms=latency,
                    metadata={"url": self.url, "status": status},
                )
            return HealthCheckResult(
                healthy=False,
                message=f"Unexpected status: {status}",
                latency_ms=latency,
                metadata={"url": self.url, "expected": self.expected_status, "actual": status},
            )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                healthy=False,
                message=f"HTTP check failed: {e}",
                latency_ms=latency,
                metadata={"url": self.url, "error": str(e)},
            )


class PortHealthCheck(HealthCheck):
    """TCP port-based health check."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 80,
        timeout: float = 5.0,
        name: str | None = None,
    ):
        super().__init__(name=name or f"port_{host}:{port}", timeout=timeout)
        self.host = host
        self.port = port

    async def run(self) -> HealthCheckResult:
        """Execute TCP port health check."""
        import asyncio
        import time

        start = time.time()
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=self.timeout,
            )
            writer.close()
            await writer.wait_closed()
            latency = (time.time() - start) * 1000

            return HealthCheckResult(
                healthy=True,
                message=f"Port {self.port} is open",
                latency_ms=latency,
                metadata={"host": self.host, "port": self.port},
            )
        except Exception as e:
            latency = (time.time() - start) * 1000
            return HealthCheckResult(
                healthy=False,
                message=f"Port check failed: {e}",
                latency_ms=latency,
                metadata={"host": self.host, "port": self.port, "error": str(e)},
            )


# Alias for backward compatibility
TCPHealthCheck = PortHealthCheck


# ============================================================================
# Module Imports
# ============================================================================

# Configuration
from .config import DeployConfig, PackageDetector  # noqa: E402

# Deployment hooks
from .hooks import (  # noqa: E402
    DeploymentHook,
    HookRegistry,
    PostDeployHook,
    PreDeployHook,
)

# Local deployment management
from .local import LocalProcessConfig, LocalServiceManager, ReadyProbe  # noqa: E402

# NVMS (Node Version Manager Script)
from .nvms import NVMSParser  # noqa: E402

# Cloud platform clients
from .platforms.fly import FlyClient  # noqa: E402
from .platforms.vercel import VercelClient  # noqa: E402

# Startup utilities
from .startup import StartupConfig, StartupManager  # noqa: E402

# Utilities
from .utils import (  # noqa: E402
    BuildHookGenerator,
    DeploymentValidator,
    EnvironmentManager,
    PlatformDetector,
    PlatformInfo,
)

# Vendoring utilities
from .vendor import PackageInfo, PhenoVendor  # noqa: E402

__version__ = "0.1.0"
__kit_name__ = "deploy"

__all__ = [
    "BuildHookGenerator",
    # Configuration
    "DeployConfig",
    # Deployment hooks
    "DeploymentHook",
    "DeploymentValidator",
    "EnvironmentManager",
    "FlyClient",
    "HTTPHealthCheck",
    # Health checks
    "HealthCheck",
    "HealthCheckResult",
    "HealthChecker",
    "HookRegistry",
    # Local deployment
    "LocalProcessConfig",
    "LocalServiceManager",
    # NVMS
    "NVMSParser",
    "PackageDetector",
    "PackageInfo",
    # Vendoring
    "PhenoVendor",
    # Utilities
    "PlatformDetector",
    "PlatformInfo",
    "PortHealthCheck",
    "PostDeployHook",
    "PreDeployHook",
    "ReadyProbe",
    "StartupConfig",
    # Startup
    "StartupManager",
    # Platform clients
    "TCPHealthCheck",
    "VercelClient",
]
