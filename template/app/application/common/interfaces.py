from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Protocol, runtime_checkable

from app.application.common.event import Event


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class SessionFactory(Protocol):
    @abstractmethod
    def __call__(self) -> AbstractAsyncContextManager[DBSession]: ...


@runtime_checkable
class Repository(Protocol):
    def __init__(self, session: DBSession) -> None: ...


class RepositoryFactory[Repo: Repository](Protocol):
    @abstractmethod
    def __call__(self, session: DBSession) -> Repo: ...


class Publisher(Protocol):
    @abstractmethod
    async def publish(self, event: Event, namespace: str) -> None: ...


class PublisherFactory(Protocol):
    @abstractmethod
    def __call__(self) -> AbstractAsyncContextManager[Publisher]: ...
