from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, kw_only=True)
class Event:
    """Base class for events."""


class EventHandler[Req: Event, Resp](Protocol):
    async def __call__(self, event: Req) -> Resp: ...
