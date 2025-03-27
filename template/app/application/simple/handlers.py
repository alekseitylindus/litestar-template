import logging

from app.application.common.command import CommandHandler
from app.application.common.event import EventHandler
from app.application.common.interfaces import (
    PublisherFactory,
    RepositoryFactory,
    SessionFactory,
)
from app.application.simple.commands import SimpleCommand
from app.application.simple.events import SimpleNumberRequestedEvent
from app.application.simple.interfaces import SimpleRepositoryProtocol

logger = logging.getLogger(__name__)


class SimpleCommandHandler(CommandHandler[SimpleCommand, int]):
    def __init__(
        self,
        session_factory: SessionFactory,
        repository_factory: RepositoryFactory[SimpleRepositoryProtocol],
        publisher_factory: PublisherFactory,
    ) -> None:
        self._session_factory = session_factory
        self._repository_factory = repository_factory
        self._publisher_factory = publisher_factory

    async def __call__(self, command: SimpleCommand) -> int:
        async with self._session_factory() as session:
            repository = self._repository_factory(session)
            result = await repository.get_simple_number(command.number)  # noqa: WPS110
            await session.commit()

        async with self._publisher_factory() as publisher:
            await publisher.publish(
                SimpleNumberRequestedEvent(
                    input_number=command.number,
                    result=result,
                ),
                namespace="simple",
            )

        return result


class SimpleNumberEventHandler(EventHandler[SimpleNumberRequestedEvent, None]):
    async def __call__(self, event: SimpleNumberRequestedEvent) -> None:
        logger.info(
            "Received SimpleNumberRequestedEvent - input_number: %d, result: %d",
            event.input_number,
            event.result,
        )
