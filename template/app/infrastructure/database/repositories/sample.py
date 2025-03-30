from typing import cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.sample.interfaces import SampleRepositoryProtocol


class SampleRepository(SampleRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_sample_number(self, number: int) -> int:
        query_result = await self._session.execute(
            text("SELECT :value * 2"),
            {"value": number},
        )
        return cast("int", query_result.scalar())
