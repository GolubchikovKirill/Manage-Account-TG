from sqlalchemy.ext.asyncio import AsyncSession
from repository.repository_channel import ChannelRepository
from fastapi import Depends
from service.session_service import TelegramSessionService
from database import get_session

def get_session_service(session: AsyncSession = Depends(get_session)):
    return TelegramSessionService(session)

# Зависимость: создаёт экземпляр репозитория сhannel.
def get_repo(session: AsyncSession = Depends(get_session)) -> ChannelRepository:
    return ChannelRepository(session)