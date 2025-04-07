from database.database import AsyncSession
from database.models import Channels
from sqlalchemy import select


class ChannelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_channel(self, name: str) -> Channels | None:
        result = await self.session.execute(
            select(Channels).filter(Channels.name == name)
        )
        return result.scalars().first()

    async def add_channel(self, name: str) -> str:
        existing_channel = await self.get_channel(name)
        if existing_channel:
            return f"Канал '{existing_channel.name}' уже существует"

        new_channel = Channels(name=name)
        self.session.add(new_channel)
        await self.session.commit()
        await self.session.refresh(new_channel)
        return f"Канал '{new_channel.name}' добавлен"

    async def remove_channel(self, name: str) -> str:
        channel = await self.get_channel(name)
        if channel:
            await self.session.delete(channel)
            await self.session.commit()
            return f"Канал '{channel.name}' удален"
        return f"Канал '{name}' не найден"