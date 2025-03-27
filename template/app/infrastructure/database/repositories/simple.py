from typing import cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.simple.interfaces import SimpleRepositoryProtocol


class SimpleRepository(SimpleRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_simple_number(self, value: int) -> int:
        result = await self._session.execute(
            text("SELECT :value * 2"),
            {"value": value},
        )
        return cast(int, result.scalar())
