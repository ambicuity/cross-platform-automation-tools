"""Logging utilities for nettools."""

import logging
import sys


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a configured logger instance.

    Args:
        name: Logger name. If None, uses 'nettools' as default.

    Returns:
        Configured logger instance.
    """
    logger_name = name or "nettools"
    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    return logger


def set_log_level(level: str) -> None:
    """Set the global log level for nettools loggers.

    Args:
        level: Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    logger = get_logger()
    logger.setLevel(numeric_level)
    for handler in logger.handlers:
        handler.setLevel(numeric_level)
