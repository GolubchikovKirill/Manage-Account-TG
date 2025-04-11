from pyrogram import Client
from service.session_service import logger


class TelegramChannelService:
    def __init__(self, client: Client):
        self.client = client

    async def get_channels(self):
        try:
            dialogs = self.client.get_dialogs()
            channels = [dialog for dialog in dialogs if dialog.chat.type == "channel"]
            return channels
        except Exception as e:
            logger.error(f"Ошибка при получении каналов: {e}")
            return []

    async def send_message_to_channel(self, channel_name: str, message: str):
        """
        Отправить сообщение в канал.
        """
        try:
            await self.client.send_message(channel_name, message)
            logger.info(f"Сообщение отправлено в канал {channel_name}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в канал {channel_name}: {e}")