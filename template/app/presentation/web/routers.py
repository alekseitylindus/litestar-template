from litestar.types import ControllerRouterHandler

from app.presentation.web.api.router import api_router

route_handlers: list[ControllerRouterHandler] = [
    api_router,
]
