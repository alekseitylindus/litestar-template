from typing import Protocol

from app.application.common.interfaces import Repository


class SimpleRepositoryProtocol(Repository, Protocol):
    """Repository for managing spaces and their bookings."""

    async def get_simple_number(self, number: int) -> int:
        """Get a simple number."""
        ...
