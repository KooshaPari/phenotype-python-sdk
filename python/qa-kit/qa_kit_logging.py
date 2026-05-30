"""Standalone logging utility for qa-kit.

Replaces the phenoSDK src.shared.logging dependency for standalone use.
"""

import logging
import sys
from functools import lru_cache
from typing import Any


def get_logger(name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """Get or create a logger with consistent formatting.

    Args:
        name: Logger name (defaults to calling module)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or "qa_kit")

    # Only add handler if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger


@lru_cache(maxsize=128)
def get_cached_logger(name: str) -> logging.Logger:
    """Get cached logger instance for better performance.

    Args:
        name: Logger name

    Returns:
        Cached logger instance
    """
    return get_logger(name)


def configure_root_logger(
    level: int = logging.INFO,
    format_string: str | None = None,
    handlers: list[logging.Handler] | None = None,
) -> None:
    """Configure the root logger for the application.

    Args:
        level: Logging level
        format_string: Custom format string
        handlers: Additional handlers to add
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    if format_string:
        formatter = logging.Formatter(format_string)
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Add any additional handlers
    if handlers:
        for handler in handlers:
            root_logger.addHandler(handler)


def set_log_level(level: int | str) -> None:
    """Set the global log level.

    Args:
        level: Logging level (int or string like 'DEBUG', 'INFO', etc.)
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    logging.getLogger().setLevel(level)
    for handler in logging.getLogger().handlers:
        handler.setLevel(level)
