from typing import Any

from dishka import Scope as DIScope
from litestar import Request
from litestar.enums import ScopeType
from litestar.middleware import AbstractMiddleware
from litestar.types import Receive, Scope, Send

from app.infrastructure.web.rate_limiter import RateLimit, RateLimiter


class RateLimitMiddleware(AbstractMiddleware):
    opt_key = "rate_limit"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        app = scope["app"]

        if scope["type"] != ScopeType.HTTP:
            await app(scope, receive, send)
            return

        rate_limit_cfg: RateLimit | None = scope["route_handler"].opt.get(self.opt_key)
        if not isinstance(rate_limit_cfg, RateLimit):
            await self.app(scope, receive, send)
            return

        request: Request[Any, Any, Any] = app.request_class(
            scope,
            receive=receive,
            send=send,
        )
        async with app.state.dishka_container(
            {Request: request},
            scope=DIScope.REQUEST,
        ) as container:
            limiter = await container.get(RateLimiter)
            await limiter(
                request,
                rate_limit_cfg.times,
                rate_limit_cfg.total_ms,
                rate_limit_cfg.identifier,
                rate_limit_cfg.callback,
            )

        await self.app(scope, receive, send)
