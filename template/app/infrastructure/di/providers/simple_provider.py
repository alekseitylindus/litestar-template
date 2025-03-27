from dishka import Provider, Scope, provide

from app.application.simple.handlers import (
    SimpleCommandHandler,
    SimpleNumberEventHandler,
)
from app.application.simple.interfaces import SimpleRepositoryProtocol
from app.infrastructure.database.repositories.simple import SimpleRepository


class SimpleProvider(Provider):
    @provide(scope=Scope.APP)
    async def repository_factory(
        self,
    ) -> type[SimpleRepositoryProtocol]:
        return SimpleRepository

    simple_command_handler = provide(SimpleCommandHandler, scope=Scope.REQUEST)
    simple_event_handler = provide(SimpleNumberEventHandler, scope=Scope.REQUEST)
