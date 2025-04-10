from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from repository.repository_channel import ChannelRepository


# Зависимость: создаёт экземпляр репозитория сhannel.
def get_repo(session: AsyncSession = Depends(get_session)) -> ChannelRepository:
    return ChannelRepository(session)