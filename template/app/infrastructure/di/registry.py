import logging

from dishka import Provider

from app.infrastructure.di.providers.app_provider import AppProvider
from app.infrastructure.di.providers.mail_provider import MailProvider
from app.infrastructure.di.providers.sample_provider import SampleProvider
from app.infrastructure.di.providers.web_provider import WebProvider

logger = logging.getLogger(__name__)


def get_providers() -> tuple[Provider, ...]:
    return (
        AppProvider(),
        WebProvider(),
        SampleProvider(),
        MailProvider(),
    )
