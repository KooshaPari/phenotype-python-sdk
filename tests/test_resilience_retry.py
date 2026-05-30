"""Tests for pheno-resilience retry module."""

from __future__ import annotations

import pytest

from pheno_resilience.retry import (
    ConstantDelayRetry,
    ExponentialBackoffRetry,
    FibonacciBackoffRetry,
    LinearBackoffRetry,
    MaxRetriesExceededError,
    RetryConfig,
    RetryStrategy,
)


class TestRetryConfig:
    """Tests for RetryConfig."""

    def test_retry_config_defaults(self) -> None:
        """Test RetryConfig default values."""
        config = RetryConfig()

        assert config.max_attempts == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.jitter is True

    def test_retry_config_custom(self) -> None:
        """Test RetryConfig with custom values."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=2.0,
            max_delay=120.0,
            jitter=False,
        )

        assert config.max_attempts == 5
        assert config.base_delay == 2.0
        assert config.max_delay == 120.0
        assert config.jitter is False


class TestExponentialBackoffRetry:
    """Tests for ExponentialBackoffRetry strategy."""

    def test_exponential_delay_calculation(self) -> None:
        """Test exponential delay calculation."""
        config = RetryConfig(max_attempts=5, jitter=False)
        strategy = ExponentialBackoffRetry(config)

        # delay = base_delay * (multiplier ** (attempt - 1))
        assert strategy.calculate_delay(1) == pytest.approx(1.0)  # 1.0 * 2^0
        assert strategy.calculate_delay(2) == pytest.approx(2.0)  # 1.0 * 2^1
        assert strategy.calculate_delay(3) == pytest.approx(4.0)  # 1.0 * 2^2

    def test_exponential_delay_max(self) -> None:
        """Test exponential delay respects max_delay."""
        config = RetryConfig(max_attempts=10, max_delay=10.0, jitter=False)
        strategy = ExponentialBackoffRetry(config)

        # Should be capped at max_delay
        assert strategy.calculate_delay(10) <= 10.0

    def test_exponential_with_custom_multiplier(self) -> None:
        """Test exponential with custom multiplier."""
        config = RetryConfig(max_attempts=5, base_delay=1.0, jitter=False)
        strategy = ExponentialBackoffRetry(config, multiplier=3.0)

        assert strategy.calculate_delay(1) == pytest.approx(1.0)   # 1.0 * 3^0
        assert strategy.calculate_delay(2) == pytest.approx(3.0)   # 1.0 * 3^1
        assert strategy.calculate_delay(3) == pytest.approx(9.0)   # 1.0 * 3^2


class TestLinearBackoffRetry:
    """Tests for LinearBackoffRetry strategy."""

    def test_linear_delay_calculation(self) -> None:
        """Test linear delay calculation."""
        config = RetryConfig(max_attempts=5, base_delay=1.0, jitter=False)
        strategy = LinearBackoffRetry(config)

        # delay = base_delay + (increment * (attempt - 1))
        assert strategy.calculate_delay(1) == pytest.approx(1.0)
        assert strategy.calculate_delay(2) == pytest.approx(2.0)
        assert strategy.calculate_delay(3) == pytest.approx(3.0)

    def test_linear_delay_max(self) -> None:
        """Test linear delay respects max_delay."""
        config = RetryConfig(max_attempts=100, base_delay=1.0, max_delay=5.0, jitter=False)
        strategy = LinearBackoffRetry(config)

        # Should be capped at max_delay
        assert strategy.calculate_delay(10) <= 5.0


class TestConstantDelayRetry:
    """Tests for ConstantDelayRetry strategy."""

    def test_constant_delay(self) -> None:
        """Test constant delay always returns base_delay."""
        config = RetryConfig(base_delay=2.0, jitter=False)
        strategy = ConstantDelayRetry(config)

        assert strategy.calculate_delay(1) == pytest.approx(2.0)
        assert strategy.calculate_delay(2) == pytest.approx(2.0)
        assert strategy.calculate_delay(100) == pytest.approx(2.0)


class TestFibonacciBackoffRetry:
    """Tests for FibonacciBackoffRetry strategy."""

    def test_fibonacci_delay(self) -> None:
        """Test Fibonacci delay calculation."""
        config = RetryConfig(base_delay=1.0, max_attempts=10, jitter=False)
        strategy = FibonacciBackoffRetry(config)

        # Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55
        fib_values = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        
        for i, expected in enumerate(fib_values, start=1):
            assert strategy.calculate_delay(i) == pytest.approx(float(expected))

    def test_fibonacci_max_delay(self) -> None:
        """Test Fibonacci delay respects max_delay."""
        config = RetryConfig(base_delay=1.0, max_attempts=20, max_delay=10.0, jitter=False)
        strategy = FibonacciBackoffRetry(config)

        # Should be capped at max_delay
        assert strategy.calculate_delay(20) <= 10.0


class TestRetryStrategy:
    """Tests for base RetryStrategy."""

    def test_should_retry_respects_max_attempts(self) -> None:
        """Test should_retry respects max_attempts."""
        config = RetryConfig(max_attempts=3)
        strategy = ExponentialBackoffRetry(config)

        exception = Exception("test error")

        # Should retry on attempts 1 and 2
        assert strategy.should_retry(1, exception) is True
        assert strategy.should_retry(2, exception) is True

        # Should not retry on attempt 3 (max_attempts)
        assert strategy.should_retry(3, exception) is False

    def test_should_retry_non_retryable_exceptions(self) -> None:
        """Test should_retry respects non_retryable_exceptions."""
        config = RetryConfig(
            max_attempts=5,
            retryable_exceptions=(ValueError,),
            non_retryable_exceptions=(TypeError,),
        )
        strategy = ExponentialBackoffRetry(config)

        # Should not retry non-retryable exceptions
        assert strategy.should_retry(1, TypeError("test")) is False

        # Should retry retryable exceptions
        assert strategy.should_retry(1, ValueError("test")) is True

    def test_execute_success(self) -> None:
        """Test execute returns result on success."""
        config = RetryConfig(max_attempts=3, jitter=False)
        strategy = ExponentialBackoffRetry(config)

        def success_func():
            return "success"

        result = strategy.execute(success_func)
        assert result == "success"

    def test_execute_failure_raises(self) -> None:
        """Test execute raises MaxRetriesExceededError on failure."""
        config = RetryConfig(max_attempts=2, jitter=False)
        strategy = ExponentialBackoffRetry(config)

        def fail_func():
            raise ValueError("Always fails")

        with pytest.raises(MaxRetriesExceededError) as exc_info:
            strategy.execute(fail_func)

        assert exc_info.value.max_attempts == 2


class TestMaxRetriesExceededError:
    """Tests for MaxRetriesExceededError."""

    def test_error_message(self) -> None:
        """Test error message format."""
        original_error = ValueError("Original error")
        error = MaxRetriesExceededError(max_attempts=3, last_exception=original_error)

        assert "Maximum retries (3)" in str(error)
        assert "Original error" in str(error)
        assert error.max_attempts == 3
        assert error.last_exception is original_error
