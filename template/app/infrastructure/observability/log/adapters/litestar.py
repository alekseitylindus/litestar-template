"""Litestar-specific logging adapters."""

from collections.abc import Sequence
from typing import Literal

from litestar.middleware.logging import LoggingMiddlewareConfig

RequestExtractorField = Literal[
    "path",
    "method",
    "content_type",
    "headers",
    "cookies",
    "query",
    "path_params",
    "body",
    "scheme",
    "client",
]

ResponseExtractorField = Literal[
    "status_code",
    "headers",
    "body",
    "cookies",
]


def get_litestar_logging_middleware_config(
    exclude_paths: str | list[str] | None = None,
    obfuscate_cookies: set[str] | None = None,
    obfuscate_headers: set[str] | None = None,
    request_fields: Sequence[RequestExtractorField] | None = None,
    response_fields: Sequence[ResponseExtractorField] | None = None,
) -> LoggingMiddlewareConfig:
    """Returns Litestar-specific middleware logging configuration."""
    return LoggingMiddlewareConfig(
        exclude=exclude_paths,
        request_cookies_to_obfuscate=obfuscate_cookies or set(),
        request_headers_to_obfuscate=obfuscate_headers or set(),
        request_log_fields=request_fields or set(),
        response_log_fields=response_fields or set(),
    )
