from typing import Any


class BaseErrorContext(dict[str, Any]):
    """Base type for error contexts."""


class DomainError[Ctx: BaseErrorContext](Exception):
    """Base exception type for the application's custom exceptions."""

    context: Ctx

    def __init__(
        self,
        message: str,
        context: Ctx,
    ) -> None:
        """Initialize DomainError.

        Args:
            message: The error message
            context: Context data for the error
        """
        super().__init__(message)
        self.context = context
