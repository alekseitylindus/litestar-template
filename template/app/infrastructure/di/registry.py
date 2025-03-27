import logging

from dishka import Provider

from app.infrastructure.di.providers.app_provider import AppProvider
from app.infrastructure.di.providers.mail_provider import MailProvider
from app.infrastructure.di.providers.simple_provider import SimpleProvider
from app.infrastructure.di.providers.web_provider import WebProvider

logger = logging.getLogger(__name__)


def get_providers() -> tuple[Provider, ...]:
    return (
        AppProvider(),
        WebProvider(),
        SimpleProvider(),
        MailProvider(),
    )
