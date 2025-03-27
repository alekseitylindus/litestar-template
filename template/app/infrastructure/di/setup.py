from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from dishka import Scope as DIScope
from litestar import Litestar, Request, WebSocket
from litestar.enums import ScopeType
from litestar.middleware import AbstractMiddleware
from litestar.types import Receive, Scope, Send


@asynccontextmanager
async def dishka_lifespan(app: Litestar) -> AsyncGenerator[None, Any]:
    yield
    await app.state.dishka_container.close()


class ContainerMiddleware(AbstractMiddleware):
    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        app = scope["app"]

        if scope["type"] not in (ScopeType.HTTP, ScopeType.WEBSOCKET):
            return await self.app(scope, receive, send)

        request: Request[Any, Any, Any] | WebSocket[Any, Any, Any]
        context: dict[
            type[Request[Any, Any, Any] | WebSocket[Any, Any, Any]],
            Request[Any, Any, Any] | WebSocket[Any, Any, Any],
        ]

        if scope["type"] == ScopeType.HTTP:
            request = app.request_class(scope, receive=receive, send=send)
            context = {Request: request}
            di_scope = DIScope.REQUEST
        else:
            request = app.websocket_class(scope, receive=receive, send=send)
            context = {WebSocket: request}
            di_scope = DIScope.SESSION

        async with request.app.state.dishka_container(
            context,
            scope=di_scope,
        ) as request_container:
            request.state.dishka_container = request_container
            return await self.app(scope, receive, send)
