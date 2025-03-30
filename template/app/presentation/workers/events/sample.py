import logging

from faststream.redis import RedisRouter

from app.application.sample.events import SampleNumberRequestedEvent
from app.application.sample.handlers import SampleNumberEventHandler
from app.infrastructure.adapters.publisher import Message
from app.presentation.workers.di import Depends

router = RedisRouter()
logger = logging.getLogger(__name__)


@router.subscriber(stream="sample")
async def sample_event(
    message: Message[SampleNumberRequestedEvent],
    interactor: Depends[SampleNumberEventHandler],
) -> None:
    logger.info("Sample event received: %s", message)
    await interactor(event=message.data)
