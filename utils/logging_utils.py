from __future__ import annotations

import logging
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar, Any

LOG_NAME = "dash_app"
LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "app.log"

CallbackType = TypeVar("CallbackType", bound=Callable[..., Any])


def setup_logging() -> logging.Logger:
    """Configure logging with file + console handlers."""
    logger = logging.getLogger(LOG_NAME)
    if logger.handlers:
        return logger

    LOG_PATH.parent.mkdir(exist_ok=True)

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False

    logger.info("Logging initialized; writing to %s", LOG_PATH)
    return logger


def get_logger() -> logging.Logger:
    """Return configured logger, initializing if needed."""
    logger = logging.getLogger(LOG_NAME)
    if not logger.handlers:
        return setup_logging()
    return logger


def log_exceptions(logger: logging.Logger) -> Callable[[CallbackType], CallbackType]:
    """Decorator to log callback exceptions while re-raising."""

    def decorator(func: CallbackType) -> CallbackType:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:  # noqa: BLE001
                logger.exception("Unhandled exception in callback %s", func.__name__)
                raise

        return wrapper  # type: ignore[return-value]

    return decorator
