from litestar import Router

from app.presentation.web.api.v1.simple import simple_endpoint

v1_router = Router(path="/v1", route_handlers=[simple_endpoint])
