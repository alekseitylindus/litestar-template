import logging

from faststream.redis import RedisRouter

from app.application.simple.events import SimpleNumberRequestedEvent
from app.application.simple.handlers import SimpleNumberEventHandler
from app.infrastructure.adapters.publisher import Message
from app.presentation.workers.di import Depends

router = RedisRouter()
logger = logging.getLogger(__name__)


@router.subscriber(stream="simple")
async def simple_event(
    message: Message[SimpleNumberRequestedEvent],
    interactor: Depends[SimpleNumberEventHandler],
) -> None:
    logger.info("Simple event received: %s", message)
    await interactor(event=message.data)
