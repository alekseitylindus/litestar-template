from dishka import Provider, Scope, provide

from app.application.sample.handlers import (
    SampleCommandHandler,
    SampleNumberEventHandler,
)
from app.application.sample.interfaces import SampleRepositoryProtocol
from app.infrastructure.database.repositories.sample import SampleRepository


class SampleProvider(Provider):
    @provide(scope=Scope.APP)
    async def repository_factory(
        self,
    ) -> type[SampleRepositoryProtocol]:
        return SampleRepository

    sample_command_handler = provide(SampleCommandHandler, scope=Scope.REQUEST)
    sample_event_handler = provide(SampleNumberEventHandler, scope=Scope.REQUEST)
