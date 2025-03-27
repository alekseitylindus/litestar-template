import contextlib
from dataclasses import dataclass
from typing import Any

from litestar import MediaType, Request, Response
from litestar.exceptions import (
    HTTPException,
)
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from litestar.types import ExceptionHandlersMap

from app.domain.exceptions.base import BaseErrorContext, DomainError


@dataclass
class ErrorResponse:
    """Standard error response structure."""

    status_code: int
    detail: str
    extra: dict[str, Any] | list[Any] | None = None
    type: str | None = None

    def to_response(
        self,
        request: Request[Any, Any, Any] | None = None,
    ) -> Response[dict[str, Any]]:
        """Convert the error response to a Litestar Response object.

        Args:
            request: Optional request object to determine media type

        Returns:
            Response: A Litestar Response with the error details.
        """
        media_type: MediaType = MediaType.JSON
        if request is not None:
            with contextlib.suppress(KeyError, AttributeError, ValueError):
                media_type = MediaType(request.route_handler.media_type)

        return Response[dict[str, Any]](
            content={
                "status_code": self.status_code,
                "detail": self.detail,
                "extra": self.extra,
                "type": self.type or "InternalError",
            },
            status_code=self.status_code,
            media_type=media_type,
        )


def domain_error_handler(
    request: Request[Any, Any, Any],
    exc: DomainError[BaseErrorContext],
) -> Response[dict[str, Any]]:
    """Handle DomainError exceptions.

    Args:
        request: The request that experienced the exception
        exc: The DomainError instance

    Returns:
        Response: A standardized error response
    """
    return ErrorResponse(
        status_code=HTTP_400_BAD_REQUEST,
        detail=str(exc),
        extra=exc.context,
        type=exc.__class__.__name__,
    ).to_response(request)


def http_exception_handler(
    request: Request[Any, Any, Any],
    exc: HTTPException,
) -> Response[dict[str, Any]]:
    """Handle HTTPException instances.

    Args:
        request: The request that experienced the exception
        exc: The HTTPException instance

    Returns:
        Response: A standardized error response
    """
    return ErrorResponse(
        status_code=exc.status_code,
        detail=exc.detail,
        type=exc.__class__.__name__,
    ).to_response(request)


def general_exception_handler(
    request: Request[Any, Any, Any],
    exc: Exception,  # noqa: ARG001
) -> Response[dict[str, Any]]:
    """Handle any unhandled exceptions.

    Args:
        request: The request that experienced the exception
        exc: The exception instance

    Returns:
        Response: A standardized error response
    """
    return ErrorResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred",
        type="InternalServerError",
    ).to_response(request)


def get_exception_handlers() -> ExceptionHandlersMap:
    """Get the mapping of exception types to their handlers.

    Returns:
        ExceptionHandlersMap: A mapping of exception types to their handler functions
    """
    return {
        DomainError: domain_error_handler,
        HTTPException: http_exception_handler,
        Exception: general_exception_handler,
    }
