from dishka import Provider, Scope, provide

from app.config.base import Settings
from app.infrastructure.mailjet.client import MailjetClient


class MailProvider(Provider):
    @provide(scope=Scope.APP)
    async def redis(self, settings: Settings) -> MailjetClient:
        return MailjetClient(
            api_key=settings.mailjet.api_key,
            api_secret=settings.mailjet.api_secret,
        )
