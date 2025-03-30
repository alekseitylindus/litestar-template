from litestar import Router

from app.presentation.web.api.v1.sample import sample_endpoint

v1_router = Router(path="/v1", route_handlers=[sample_endpoint])
