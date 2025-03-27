from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, kw_only=True)
class Command:
    """Base class for commands."""


class CommandHandler[Req: Command, Resp](Protocol):
    async def __call__(self, command: Req) -> Resp: ...
