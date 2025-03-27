"""Test doubles for application layer event publishing."""

from collections import defaultdict
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from app.application.common.event import Event
from app.application.common.interfaces import Publisher, PublisherFactory


class InMemoryPublisher(Publisher):
    """A Publisher implementation that stores events in memory for testing."""

    def __init__(self) -> None:
        self.published_events: dict[str, list[Event]] = defaultdict(list)

    async def publish(self, event: Event, namespace: str) -> None:
        """Store the event in memory under the specified namespace."""
        self.published_events[namespace].append(event)

    def get_events(self, namespace: str) -> list[Event]:
        """Get all events published to the specified namespace."""
        return self.published_events[namespace]

    def clear(self) -> None:
        """Clear all stored events."""
        self.published_events.clear()


class InMemoryPublisherFactory(PublisherFactory):
    """Factory that creates InMemoryPublisher instances within an async context."""

    def __init__(self) -> None:
        self.publisher = InMemoryPublisher()

    def __call__(self) -> AbstractAsyncContextManager[Publisher]:
        @asynccontextmanager
        async def factory() -> AsyncIterator[Publisher]:
            yield self.publisher

        return factory()
