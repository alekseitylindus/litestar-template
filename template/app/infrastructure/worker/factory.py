import logging.config  # noqa: WPS301

from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream

from app.config.base import Settings, get_settings
from app.infrastructure.di.registry import get_providers
from app.infrastructure.observability.log.config import get_logging_config
from app.infrastructure.observability.sentry import configure_sentry
from app.infrastructure.worker.broker import get_broker
from app.presentation.workers.router import router


def create_app() -> FastStream:
    """Create and configure the FastStream worker application."""
    settings = get_settings()

    logging_config = get_logging_config(level=settings.log.level)
    logging.config.dictConfig(logging_config)

    configure_sentry(
        dsn=settings.app.sentry_dsn,
        environment=settings.app.sentry_env,
        integrations=[],
    )

    container = make_async_container(
        *get_providers(),
        context={Settings: settings},
    )

    broker = get_broker(settings.redis.url, db=settings.redis.broker_db)
    broker.include_router(router)
    app = FastStream(broker)
    setup_dishka(container, app, auto_inject=True)
    return app
