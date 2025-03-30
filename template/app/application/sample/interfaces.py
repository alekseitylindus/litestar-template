from typing import Protocol

from app.application.common.interfaces import Repository


class SampleRepositoryProtocol(Repository, Protocol):
    """Repository for managing spaces and their bookings."""

    async def get_sample_number(self, number: int) -> int:
        """Get a sample number."""
        ...
