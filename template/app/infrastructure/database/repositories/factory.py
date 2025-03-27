from collections.abc import Callable
from typing import TypeVar

from app.application.common.interfaces import DBSession, Repository, RepositoryFactory

Repo = TypeVar("Repo", bound="Repository")


class ConcreteRepositoryFactory(RepositoryFactory[Repo]):
    def __init__(self, factory: Callable[[DBSession], Repo]) -> None:
        self._factory = factory

    def __call__(self, session: DBSession) -> Repo:
        return self._factory(session)
