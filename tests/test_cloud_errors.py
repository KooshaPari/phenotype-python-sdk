"""Tests for cloud error handling module."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from pheno_deploy_kit.cloud.errors import (
    AuthenticationError,
    CloudError,
    ConflictError,
    ErrorCategory,
    NetworkError,
    NotSupportedError,
    ProvisioningError,
    QuotaError,
    ResourceNotFoundError,
    RetryConfig,
    ValidationError,
    calculate_backoff,
    should_retry,
    wrap_error,
)


class TestCloudError:
    """Tests for CloudError base class."""

    def test_cloud_error_basic(self) -> None:
        """Test basic CloudError creation."""
        error = CloudError(
            category=ErrorCategory.VALIDATION,
            code="TEST_ERROR",
            message="Test error message",
        )

        assert error.category == ErrorCategory.VALIDATION
        assert error.code == "TEST_ERROR"
        assert error.message == "Test error message"
        assert not error.retryable

    def test_cloud_error_with_provider(self) -> None:
        """Test CloudError with provider."""
        error = CloudError(
            category=ErrorCategory.NETWORK,
            code="NETWORK_ERR",
            message="Network error",
            provider="aws",
        )

        assert error.provider == "aws"
        assert "aws" in str(error)
        assert "NETWORK" in str(error)

    def test_cloud_error_retryable(self) -> None:
        """Test CloudError with retryable flag."""
        error = CloudError(
            category=ErrorCategory.QUOTA,
            code="QUOTA_ERR",
            message="Quota exceeded",
            retryable=True,
        )

        assert error.retryable is True

    def test_cloud_error_with_cause(self) -> None:
        """Test CloudError with cause exception."""
        cause = ValueError("Original error")
        error = CloudError(
            category=ErrorCategory.INTERNAL,
            code="INTERNAL_ERR",
            message="Internal error",
            cause=cause,
        )

        assert error.cause is cause


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_authentication_error(self) -> None:
        """Test AuthenticationError creation."""
        error = AuthenticationError(
            provider="aws",
            message="Invalid credentials",
        )

        assert error.category == ErrorCategory.AUTHENTICATION
        assert error.code == "AUTH_FAILED"
        assert error.provider == "aws"
        assert not error.retryable


class TestQuotaError:
    """Tests for QuotaError."""

    def test_quota_error(self) -> None:
        """Test QuotaError creation."""
        error = QuotaError(
            provider="aws",
            message="Limit exceeded",
            limit=100,
            current=100,
        )

        assert error.category == ErrorCategory.QUOTA
        assert error.code == "QUOTA_EXCEEDED"
        assert error.limit == 100
        assert error.current == 100
        assert error.retryable

    def test_quota_error_with_reset_time(self) -> None:
        """Test QuotaError with reset time."""
        reset_time = datetime.now() + timedelta(hours=1)
        error = QuotaError(
            provider="gcp",
            message="Rate limit",
            limit=1000,
            current=1500,
            reset_time=reset_time,
        )

        assert error.reset_time == reset_time


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error(self) -> None:
        """Test ValidationError creation."""
        error = ValidationError(
            provider="vercel",
            field="timeout",
            message="Invalid value",
        )

        assert error.category == ErrorCategory.VALIDATION
        assert error.code == "INVALID_CONFIG"
        assert error.field == "timeout"
        assert not error.retryable


class TestResourceNotFoundError:
    """Tests for ResourceNotFoundError."""

    def test_resource_not_found_error(self) -> None:
        """Test ResourceNotFoundError creation."""
        error = ResourceNotFoundError(
            provider="aws",
            resource_id="i-1234567890abcdef0",
        )

        assert error.category == ErrorCategory.NOT_FOUND
        assert error.code == "RESOURCE_NOT_FOUND"
        assert error.resource_id == "i-1234567890abcdef0"
        assert not error.retryable


class TestConflictError:
    """Tests for ConflictError."""

    def test_conflict_error(self) -> None:
        """Test ConflictError creation."""
        error = ConflictError(
            provider="aws",
            message="Resource already exists",
            conflicting_resource="arn:aws:ec2:...",
        )

        assert error.category == ErrorCategory.CONFLICT
        assert error.code == "RESOURCE_CONFLICT"
        assert error.conflicting_resource == "arn:aws:ec2:..."


class TestProvisioningError:
    """Tests for ProvisioningError."""

    def test_provisioning_error(self) -> None:
        """Test ProvisioningError creation."""
        error = ProvisioningError(
            provider="aws",
            phase="CREATE",
            message="Failed to create resource",
        )

        assert error.category == ErrorCategory.PROVISIONING
        assert error.code == "PROVISIONING_FAILED"
        assert error.phase == "CREATE"
        assert error.retryable


class TestNetworkError:
    """Tests for NetworkError."""

    def test_network_error(self) -> None:
        """Test NetworkError creation."""
        error = NetworkError(
            provider="aws",
            endpoint="https://example.com",
            message="Connection refused",
        )

        assert error.category == ErrorCategory.NETWORK
        assert error.code == "NETWORK_ERROR"
        assert error.endpoint == "https://example.com"
        assert error.retryable


class TestNotSupportedError:
    """Tests for NotSupportedError."""

    def test_not_supported_error(self) -> None:
        """Test NotSupportedError creation."""
        error = NotSupportedError(
            provider="aws",
            operation="batch_deploy",
        )

        assert error.category == ErrorCategory.NOT_SUPPORTED
        assert error.code == "NOT_SUPPORTED"
        assert error.operation == "batch_deploy"
        assert not error.retryable


class TestRetryConfig:
    """Tests for RetryConfig."""

    def test_retry_config_defaults(self) -> None:
        """Test RetryConfig default values."""
        config = RetryConfig()

        assert config.max_retries == 5
        assert config.initial_delay == timedelta(seconds=1)
        assert config.max_delay == timedelta(seconds=16)
        assert config.multiplier == 2.0
        assert config.jitter is True

    def test_retry_config_custom(self) -> None:
        """Test RetryConfig with custom values."""
        config = RetryConfig(
            max_retries=10,
            initial_delay=timedelta(seconds=0.5),
            max_delay=timedelta(seconds=30),
            jitter=False,
        )

        assert config.max_retries == 10
        assert config.initial_delay == timedelta(seconds=0.5)
        assert config.max_delay == timedelta(seconds=30)
        assert config.jitter is False


class TestShouldRetry:
    """Tests for should_retry function."""

    def test_should_retry_cloud_error_retryable(self) -> None:
        """Test should_retry with retryable CloudError."""
        error = QuotaError(
            provider="aws",
            message="Quota exceeded",
            limit=100,
            current=100,
        )
        config = RetryConfig()

        assert should_retry(error, config) is True

    def test_should_retry_cloud_error_not_retryable(self) -> None:
        """Test should_retry with non-retryable CloudError."""
        error = ValidationError(
            provider="aws",
            field="name",
            message="Invalid",
        )
        config = RetryConfig()

        assert should_retry(error, config) is False

    def test_should_retry_connection_error(self) -> None:
        """Test should_retry with ConnectionError."""
        error = ConnectionError("Connection refused")
        config = RetryConfig()

        assert should_retry(error, config) is True

    def test_should_retry_timeout_error(self) -> None:
        """Test should_retry with TimeoutError."""
        error = TimeoutError("Operation timed out")
        config = RetryConfig()

        assert should_retry(error, config) is True

    def test_should_retry_regular_exception(self) -> None:
        """Test should_retry with regular exception."""
        error = ValueError("Invalid value")
        config = RetryConfig()

        assert should_retry(error, config) is False


class TestCalculateBackoff:
    """Tests for calculate_backoff function."""

    def test_calculate_backoff_basic(self) -> None:
        """Test basic backoff calculation."""
        config = RetryConfig(max_retries=5, jitter=False)
        delay = calculate_backoff(0, config)

        # First attempt: initial_delay
        assert delay == timedelta(seconds=1)

    def test_calculate_backoff_exponential(self) -> None:
        """Test exponential backoff calculation."""
        config = RetryConfig(max_retries=5, multiplier=2.0, jitter=False)
        
        delay0 = calculate_backoff(0, config)  # 1s
        delay1 = calculate_backoff(1, config)  # 2s
        delay2 = calculate_backoff(2, config)  # 4s

        assert delay0 == timedelta(seconds=1)
        assert delay1 == timedelta(seconds=2)
        assert delay2 == timedelta(seconds=4)

    def test_calculate_backoff_max_delay(self) -> None:
        """Test backoff respects max delay."""
        config = RetryConfig(
            max_retries=10,
            initial_delay=timedelta(seconds=1),
            max_delay=timedelta(seconds=10),
            jitter=False,
        )
        
        delay = calculate_backoff(10, config)  # Would be 1024s but capped

        assert delay <= timedelta(seconds=10)

    def test_calculate_backoff_with_jitter(self) -> None:
        """Test backoff with jitter applied."""
        config = RetryConfig(max_retries=5, jitter=True)
        delays = [calculate_backoff(0, config) for _ in range(10)]

        # Jitter should produce some variation
        unique_delays = set(str(d.total_seconds()) for d in delays)
        assert len(unique_delays) > 1

    def test_calculate_backoff_max_retries_exceeded(self) -> None:
        """Test backoff returns zero when max retries exceeded."""
        config = RetryConfig(max_retries=5)
        delay = calculate_backoff(10, config)

        assert delay == timedelta(0)


class TestWrapError:
    """Tests for wrap_error function."""

    def test_wrap_error_network(self) -> None:
        """Test wrap_error for network category."""
        original = ConnectionError("Connection failed")
        wrapped = wrap_error(
            provider="aws",
            category=ErrorCategory.NETWORK,
            message="Cloud network error",
            error=original,
        )

        assert isinstance(wrapped, CloudError)
        assert wrapped.category == ErrorCategory.NETWORK
        assert wrapped.cause is original
        assert wrapped.retryable is True

    def test_wrap_error_validation(self) -> None:
        """Test wrap_error for validation category."""
        original = ValueError("Invalid input")
        wrapped = wrap_error(
            provider="gcp",
            category=ErrorCategory.VALIDATION,
            message="Cloud validation error",
            error=original,
        )

        assert isinstance(wrapped, CloudError)
        assert wrapped.category == ErrorCategory.VALIDATION
        assert wrapped.retryable is False
