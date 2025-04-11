from fastapi import APIRouter, HTTPException, Depends
from typing import List
from depends.depends import get_session_service
from service.session_service import TelegramSessionService
from service.openai_service import generate_comment
from schema_pydantic.schemas import ChannelOut

from service.channel_service import TelegramChannelService

router = APIRouter(prefix="/channels", tags=["channels"])


@router.get("/", response_model=List[ChannelOut])
async def get_channels(account_id: int, session_service: TelegramSessionService = Depends(get_session_service)):
    """
    Получаем список каналов, к которым подключен аккаунт.
    """
    client = await session_service.get_client(account_id)
    if not client:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")

    channel_service = TelegramChannelService(client)
    channels = await channel_service.get_channels()
    if not channels:
        raise HTTPException(status_code=404, detail="Нет каналов")

    return channels


@router.post("/generate-comment", response_model=str)
async def generate_comment_for_post(post_text: str):
    """
    Генерация комментария для поста.
    """
    try:
        comment = await generate_comment(post_text)
        return comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации комментария: {str(e)}")


@router.post("/send-comment")
async def send_comment_to_channel(account_id: int, channel_name: str, post_text: str,
                                  session_service: TelegramSessionService = Depends(get_session_service)):
    """
    Генерация комментария и отправка его на выбранный канал.
    """
    # Получаем клиента для аккаунта
    client = await session_service.get_client(account_id)
    if not client:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")

    # Получаем список каналов
    channel_service = TelegramChannelService(client)
    channels = await channel_service.get_channels()

    # Проверяем, что канал существует
    channel = next((ch for ch in channels if ch.chat.title == channel_name), None)
    if not channel:
        raise HTTPException(status_code=404, detail=f"Канал {channel_name} не найден")

    # Генерируем комментарий для поста
    comment = await generate_comment(post_text)

    # Отправляем комментарий на канал
    await channel_service.send_message_to_channel(channel_name, comment)

    return {"message": "Комментарий отправлен успешно", "channel": channel_name}