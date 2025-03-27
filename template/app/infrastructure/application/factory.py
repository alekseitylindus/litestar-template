import logging.config  # noqa: WPS301 logging here

from dishka import make_async_container
from litestar import Litestar
from litestar.datastructures import State
from litestar.types import Middleware
from sentry_sdk.integrations.litestar import LitestarIntegration

from app.config.base import Settings, get_settings
from app.infrastructure.application.app_configs import (
    get_compression_config,
    get_cors_config,
    get_csrf_config,
)
from app.infrastructure.application.middleware.rate_limit import RateLimitMiddleware
from app.infrastructure.application.openapi import get_openapi_config
from app.infrastructure.application.plugins import get_plugins
from app.infrastructure.application.templates import get_template_config
from app.infrastructure.di.registry import get_providers
from app.infrastructure.di.setup import ContainerMiddleware, dishka_lifespan
from app.infrastructure.observability.log.adapters.litestar import (
    get_litestar_logging_middleware_config,
)
from app.infrastructure.observability.log.config import get_logging_config
from app.infrastructure.observability.sentry import configure_sentry
from app.presentation.web.exception_handlers import get_exception_handlers
from app.presentation.web.routers import route_handlers


def create_app() -> Litestar:  # noqa: WPS210 allowed for app setup
    """Create and configure the Litestar application."""
    settings = get_settings()

    logging_config = get_logging_config(level=settings.log.level)
    logging.config.dictConfig(logging_config)

    plugins = get_plugins(settings)
    middleware_config = get_litestar_logging_middleware_config(
        exclude_paths=settings.log.exclude_paths,
        obfuscate_cookies=settings.log.obfuscate_cookies,
        obfuscate_headers=settings.log.obfuscate_headers,
        request_fields=settings.log.request_fields,
        response_fields=settings.log.response_fields,
    )
    middleware: list[Middleware] = [
        ContainerMiddleware,
        RateLimitMiddleware,
        middleware_config.middleware,
    ]

    configure_sentry(
        dsn=settings.app.sentry_dsn,
        environment=settings.app.sentry_env,
        integrations=[LitestarIntegration()],
    )

    container = make_async_container(
        *get_providers(),
        context={Settings: settings},
    )

    return Litestar(
        route_handlers=route_handlers,
        debug=settings.app.debug,
        openapi_config=get_openapi_config(settings),
        compression_config=get_compression_config(settings),
        template_config=get_template_config(settings),
        csrf_config=get_csrf_config(settings),
        cors_config=get_cors_config(settings),
        plugins=plugins,
        middleware=middleware,
        lifespan=[dishka_lifespan],
        exception_handlers=get_exception_handlers(),
        state=State(
            state={
                "dishka_container": container,
            },
        ),
    )
