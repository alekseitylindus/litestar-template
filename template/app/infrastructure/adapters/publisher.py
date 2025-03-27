"""Redis Streams implementation of the Publisher protocol using FastStream."""

import inspect
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from faststream.redis import RedisBroker
from pydantic import BaseModel, Field

from app.application.common.event import Event
from app.application.common.interfaces import Publisher, PublisherFactory


class Message[Payload: Event](BaseModel):
    id: UUID = Field(default_factory=uuid4)
    time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    type: str
    source: str
    data: Payload  # noqa: WPS110 generic name for generic use


class EventPublisher(Publisher):
    """Publisher implementation that uses Redis Streams via FastStream."""

    def __init__(self, broker: RedisBroker) -> None:
        self._broker = broker

    async def publish(self, event: Event, namespace: str) -> None:
        message: Message[Event] = Message(
            type=_get_full_path(type(event)),
            source=_caller_path(),
            data=event,
        )
        await self._broker.publish(message=message, stream=namespace)


class EventPublisherFactory(PublisherFactory):
    """Factory that creates EventPublisher instances within an async context."""

    def __init__(self, broker: RedisBroker) -> None:
        self._broker = broker

    def __call__(self) -> AbstractAsyncContextManager[Publisher]:
        @asynccontextmanager
        async def factory() -> AsyncIterator[Publisher]:
            yield EventPublisher(self._broker)

        return factory()


def _get_full_path(class_or_instance: Any) -> str:
    class_type = class_or_instance if isinstance(class_or_instance, type) else type(class_or_instance)
    module = class_type.__module__
    qualname = class_type.__qualname__
    return qualname if module in (None, "__builtin__") else f"{module}.{qualname}"


def _caller_path(skip: int = 1) -> str:
    frame = inspect.currentframe()
    for _ in range(skip + 1):
        if not frame:
            return ""
        frame = frame.f_back

    if not frame:
        return ""

    parts = []
    # Module/package
    module = frame.f_globals.get("__name__", "")
    if module:
        parts.extend(module.split("."))

    # Class detection
    self_obj = frame.f_locals.get("self")
    if self_obj is not None:
        parts.append(self_obj.__class__.__name__)

    # Function/method
    func_name = frame.f_code.co_name
    if func_name != "<module>":
        parts.append(func_name)

    return ".".join(parts)
