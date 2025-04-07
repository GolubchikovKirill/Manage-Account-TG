from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from settings import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.DB_URL, echo=True)

async_session = async_sessionmaker(engine,
                             expire_on_commit=False,
                             class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
