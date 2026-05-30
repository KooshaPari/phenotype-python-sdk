"""Tests for pheno-resilience circuit breaker module."""

from __future__ import annotations

import pytest

from pheno_resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitBreakerOpenError,
    CircuitBreakerState,
)


class TestCircuitBreakerConfig:
    """Tests for CircuitBreakerConfig."""

    def test_config_defaults(self) -> None:
        """Test CircuitBreakerConfig default values."""
        config = CircuitBreakerConfig()

        assert config.failure_threshold == 5
        assert config.failure_window == 60.0
        assert config.recovery_timeout == 30.0
        assert config.success_threshold == 3
        assert config.enable_monitoring is True

    def test_config_custom(self) -> None:
        """Test CircuitBreakerConfig with custom values."""
        config = CircuitBreakerConfig(
            failure_threshold=10,
            failure_window=120.0,
            recovery_timeout=60.0,
            success_threshold=5,
        )

        assert config.failure_threshold == 10
        assert config.failure_window == 120.0
        assert config.recovery_timeout == 60.0
        assert config.success_threshold == 5


class TestCircuitBreakerState:
    """Tests for CircuitBreakerState enum."""

    def test_states_exist(self) -> None:
        """Test all expected states exist."""
        assert CircuitBreakerState.CLOSED is not None
        assert CircuitBreakerState.OPEN is not None
        assert CircuitBreakerState.HALF_OPEN is not None

    def test_state_values(self) -> None:
        """Test state string values."""
        assert CircuitBreakerState.CLOSED.value == "closed"
        assert CircuitBreakerState.OPEN.value == "open"
        assert CircuitBreakerState.HALF_OPEN.value == "half_open"


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_circuit_breaker_initialization(self) -> None:
        """Test CircuitBreaker initialization."""
        circuit = CircuitBreaker(name="test_circuit")

        assert circuit.name == "test_circuit"
        assert circuit.state == CircuitBreakerState.CLOSED
        assert circuit.failure_count == 0
        assert circuit.success_count == 0

    def test_circuit_starts_closed(self) -> None:
        """Test circuit starts in closed state."""
        circuit = CircuitBreaker(name="test")

        assert circuit.is_closed
        assert not circuit.is_open
        assert not circuit.is_half_open

    def test_call_success(self) -> None:
        """Test successful call through circuit breaker."""
        circuit = CircuitBreaker(name="test")

        def success_func():
            return "success"

        result = circuit.call(success_func)
        assert result == "success"
        assert circuit.success_count == 1
        assert circuit.is_closed

    def test_call_failure_records_failure(self) -> None:
        """Test failure is recorded."""
        circuit = CircuitBreaker(name="test", config=CircuitBreakerConfig(failure_threshold=3))

        def fail_func():
            raise ValueError("test error")

        with pytest.raises(ValueError):
            circuit.call(fail_func)

        assert circuit.failure_count == 1
        # total_failures is accessed via get_stats()
        stats = circuit.get_stats()
        assert stats["total_failures"] == 1

    def test_circuit_opens_after_threshold(self) -> None:
        """Test circuit opens after failure threshold."""
        circuit = CircuitBreaker(name="test", config=CircuitBreakerConfig(failure_threshold=2))

        def fail_func():
            raise ValueError("test error")

        # Fail twice to open circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                circuit.call(fail_func)

        assert circuit.is_open

    def test_open_circuit_raises_error(self) -> None:
        """Test calling through open circuit raises error."""
        config = CircuitBreakerConfig(failure_threshold=1, recovery_timeout=0.1)
        circuit = CircuitBreaker(name="test", config=config)

        def fail_func():
            raise ValueError("test error")

        # Open the circuit
        with pytest.raises(ValueError):
            circuit.call(fail_func)

        assert circuit.is_open

        # Next call should raise CircuitBreakerOpenError
        with pytest.raises(CircuitBreakerOpenError):
            circuit.call(success_func := lambda: "success")

    def test_reset_circuit(self) -> None:
        """Test resetting circuit breaker."""
        circuit = CircuitBreaker(name="test", config=CircuitBreakerConfig(failure_threshold=1))

        def fail_func():
            raise ValueError("test error")

        # Open the circuit
        with pytest.raises(ValueError):
            circuit.call(fail_func)

        assert circuit.is_open

        # Reset
        circuit.reset()

        assert circuit.is_closed
        assert circuit.failure_count == 0
        assert circuit.success_count == 0

    def test_get_stats(self) -> None:
        """Test getting circuit breaker statistics."""
        circuit = CircuitBreaker(name="test")

        def success_func():
            return "success"

        circuit.call(success_func)

        stats = circuit.get_stats()

        assert stats["name"] == "test"
        assert stats["state"] == "closed"
        assert stats["total_calls"] == 1
        assert stats["total_successes"] == 1
        assert stats["total_failures"] == 0


class TestCircuitBreakerOpenError:
    """Tests for CircuitBreakerOpenError."""

    def test_error_message(self) -> None:
        """Test error message format."""
        error = CircuitBreakerOpenError(
            circuit_name="test_circuit",
            state=CircuitBreakerState.OPEN,
        )

        assert "test_circuit" in str(error)
        assert "open" in str(error)
        assert error.circuit_name == "test_circuit"
        assert error.state == CircuitBreakerState.OPEN

    def test_error_inherits_from_circuit_breaker_error(self) -> None:
        """Test CircuitBreakerOpenError inheritance."""
        error = CircuitBreakerOpenError(
            circuit_name="test",
            state=CircuitBreakerState.OPEN,
        )

        assert isinstance(error, CircuitBreakerError)
        assert isinstance(error, Exception)


class TestCircuitBreakerError:
    """Tests for CircuitBreakerError base exception."""

    def test_base_exception(self) -> None:
        """Test base CircuitBreakerError."""
        error = CircuitBreakerError("Circuit error")

        assert str(error) == "Circuit error"
        assert isinstance(error, Exception)
