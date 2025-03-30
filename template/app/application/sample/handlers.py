import logging

from app.application.common.command import CommandHandler
from app.application.common.event import EventHandler
from app.application.common.interfaces import (
    PublisherFactory,
    RepositoryFactory,
    SessionFactory,
)
from app.application.sample.commands import SampleCommand
from app.application.sample.events import SampleNumberRequestedEvent
from app.application.sample.interfaces import SampleRepositoryProtocol

logger = logging.getLogger(__name__)


class SampleCommandHandler(CommandHandler[SampleCommand, int]):
    def __init__(
        self,
        session_factory: SessionFactory,
        repository_factory: RepositoryFactory[SampleRepositoryProtocol],
        publisher_factory: PublisherFactory,
    ) -> None:
        self._session_factory = session_factory
        self._repository_factory = repository_factory
        self._publisher_factory = publisher_factory

    async def __call__(self, command: SampleCommand) -> int:
        async with self._session_factory() as session:
            repository = self._repository_factory(session)
            result = await repository.get_sample_number(command.number)  # noqa: WPS110
            await session.commit()

        async with self._publisher_factory() as publisher:
            await publisher.publish(
                SampleNumberRequestedEvent(
                    input_number=command.number,
                    result=result,
                ),
                namespace="sample",
            )

        return result


class SampleNumberEventHandler(EventHandler[SampleNumberRequestedEvent, None]):
    async def __call__(self, event: SampleNumberRequestedEvent) -> None:
        logger.info(
            "Received SampleNumberRequestedEvent - input_number: %d, result: %d",
            event.input_number,
            event.result,
        )
