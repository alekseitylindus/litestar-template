"""Module contains logs formatters."""

from logging import Formatter, LogRecord

from pythonjsonlogger.json import JsonFormatter

BUILTIN_ATTRS = frozenset(
    (
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
        "taskName",
        "status_code",  # custom field
        "request",  # custom field
    )
)


def format_record(record: LogRecord) -> LogRecord:
    """Moves all additional data in log record to field 'extra_data'."""
    extra_data = {
        key: value
        for key, value in record.__dict__.items()  # noqa: WPS110
        if key not in BUILTIN_ATTRS
    }

    for key in extra_data:
        record.__dict__.pop(key, None)

    record.__dict__["extra_data"] = (
        "; ".join(f"{key}: {value}" for key, value in extra_data.items())  # noqa: WPS110, WPS441
        if extra_data
        else ""
    )

    return record


class LogsFormatter(Formatter):
    """Formatter for logs."""

    def format(self, record: LogRecord) -> str:
        """Format logs."""
        formatted_record = format_record(record)
        return super().format(formatted_record)


class JsonLogsFormatter(JsonFormatter):
    """Formatter for json logs."""

    def format(self, record: LogRecord) -> str:
        """Format logs."""
        formatted_record = format_record(record)
        return super().format(formatted_record)
