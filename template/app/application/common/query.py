from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, kw_only=True)
class Query:
    """Base class for queries."""


class QueryHandler[Req: Query, Resp](Protocol):
    async def __call__(self, query: Req) -> Resp: ...
