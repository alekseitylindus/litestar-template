from litestar import Router

from app.presentation.web.api.v1.router import v1_router

api_router = Router(path="/api", route_handlers=[v1_router])
