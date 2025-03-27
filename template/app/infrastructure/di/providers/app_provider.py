import logging
from collections.abc import AsyncIterable
from urllib.parse import urlsplit

from aiocache import RedisCache
from aiocache.serializers import PickleSerializer
from dishka import Provider, Scope, from_context, provide  # noqa: WPS347
from faststream.redis import RedisBroker
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine

from app.application.common.interfaces import (
    PublisherFactory,
    RepositoryFactory,
    SessionFactory,
)
from app.config.base import Settings
from app.infrastructure.adapters.publisher import EventPublisherFactory
from app.infrastructure.database.repositories.factory import (
    ConcreteRepositoryFactory,
    Repo,
)
from app.infrastructure.database.session import get_async_session_maker, get_engine
from app.infrastructure.worker.broker import get_broker

logger = logging.getLogger(__name__)


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def cache(self, settings: Settings) -> AsyncIterable[RedisCache]:
        redis_url = urlsplit(settings.redis.url)
        cache = RedisCache(
            namespace="cache",
            serializer=PickleSerializer(),
            endpoint=redis_url.hostname,
            port=redis_url.port,
            db=settings.redis.general_db,
            password=redis_url.password,
            create_connection_timeout=settings.redis.socket_connect_timeout,
        )
        yield cache
        await cache.close()

    @provide(scope=Scope.APP)
    async def redis(self, redis_cache: RedisCache) -> AsyncIterable[Redis]:
        yield redis_cache.client

    @provide(scope=Scope.APP)
    async def engine(self, settings: Settings) -> AsyncIterable[AsyncEngine]:
        engine = get_engine(
            url=settings.db.url,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
            echo=settings.db.echo,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def session_factory(
        self,
        engine: AsyncEngine,
    ) -> SessionFactory:
        return get_async_session_maker(engine)

    @provide(scope=Scope.APP)
    def make_repository_factory(
        self,
        repository_type: type[Repo],
    ) -> RepositoryFactory[Repo]:
        return ConcreteRepositoryFactory(repository_type)

    @provide(scope=Scope.APP)
    async def redis_broker(self, settings: Settings) -> AsyncIterable[RedisBroker]:
        broker = get_broker(settings.redis.url, db=settings.redis.broker_db)
        async with broker:
            yield broker

    @provide(scope=Scope.REQUEST)
    def publisher_factory(self, broker: RedisBroker) -> PublisherFactory:
        return EventPublisherFactory(broker)
