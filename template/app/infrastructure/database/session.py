from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def get_engine(
    url: str, pool_size: int = 5, max_overflow: int = 10, *, echo: bool = False
) -> AsyncEngine:
    engine = create_async_engine(
        url=url,
        pool_pre_ping=True,
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=echo,
    )
    return engine


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
