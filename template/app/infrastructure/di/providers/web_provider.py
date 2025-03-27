from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from app.infrastructure.web.rate_limiter import RateLimiter


class WebProvider(Provider):
    @provide(scope=Scope.APP)
    async def rate_limiter(self, redis: Redis) -> RateLimiter:
        return await RateLimiter.setup(
            redis,
            prefix="rate_limiter",
        )
