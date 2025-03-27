import logging
from http import HTTPStatus
from typing import cast

import httpx

from app.infrastructure.mailjet.types import (
    JSON,
    MailjetMessagePayload,
    MailjetSendMessagesResponse,
)

logger = logging.getLogger(__name__)


class MailjetClient:
    def __init__(self, api_key: str, api_secret: str, timeout: float = 5.0) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.mailjet.com/v3.1"
        self.timeout = timeout

    async def send_email(
        self, messages: list[MailjetMessagePayload]
    ) -> MailjetSendMessagesResponse:
        endpoint = "send"
        payload = {
            "Messages": messages,
        }
        response = await self._call_api("POST", endpoint, data=cast(JSON, payload))
        if response.status_code != HTTPStatus.OK:
            logger.error(
                "Failed to send email. Mailjet returned %d status code. Response: %s",
                response.status_code,
                response.text,
            )
            msg = "Failed to send email"
            raise MailjetAPIError(msg)

        return cast(MailjetSendMessagesResponse, response.json())

    async def _call_api(
        self,
        method: str,
        endpoint: str,
        data: JSON | None = None,  # noqa: WPS110 generic name for generic method
    ) -> httpx.Response:
        url = f"{self.base_url}/{endpoint}"
        auth = httpx.BasicAuth(username=self.api_key, password=self.api_secret)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method,
                    url,
                    headers={
                        "Content-Type": "application/json",
                    },
                    json=data,
                    auth=auth,
                    timeout=self.timeout,
                )
            except httpx.TimeoutException:
                msg = "Request timed out"
                raise TimeoutError(msg) from None
            except httpx.RequestError as exc:
                msg = f"Request failed: {exc}"
                raise MailjetAPIError(msg) from None
            return response


class MailjetAPIError(Exception):
    """Error raised when a Mailjet API request fails."""
