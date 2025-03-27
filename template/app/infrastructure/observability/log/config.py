"""Core logging configuration."""

from typing import Any


def get_logging_config(level: str) -> dict[str, Any]:
    """Returns a dictionary for logging configuration.

    Args:
        level: The logging level to use.

    Returns:
        A dictionary suitable for use with logging.config.dictConfig.
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(levelname)s - %(asctime)s - %(process)d:%(taskName)-7s - %(name)s:%(lineno)d - %(message)s %(extra_data)s",
                "()": "app.infrastructure.observability.log.formatters.LogsFormatter",
            },
            "json": {
                "format": "%(levelname)s %(asctime)s %(pathname)s:%(lineno)d %(process)d %(message)s %(extra_data)s",
                "()": "app.infrastructure.observability.log.formatters.JsonLogsFormatter",
                "json_ensure_ascii": False,
            },
        },
        "handlers": {
            "queue_listener": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "app": {
                "handlers": ["queue_listener"],
                "level": level,
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["queue_listener"],
            "level": "WARNING",
        },
    }
