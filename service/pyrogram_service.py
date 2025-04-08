"""
    Получение сессии, имитация авторизации из папки tdata файлов .session
"""
import asyncio
import os
from pyrogram import Client
from settings import settings


class PyrogramService:
    def __init__(self, session_name: str):
        self.session_name = session_name
        self.base_dir = os.path.abspath(os.path.join("tdata", session_name))
        os.makedirs(self.base_dir, exist_ok=True)  # Создаем папку, если её нет

        self.client = Client(
            name=session_name,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            workdir=self.base_dir,
            in_memory=False
        )

    async def start(self):
        """Запуск клиента с обработкой исключений"""
        try:
            await self.client.start()
            print(f"Успешный запуск сессии: {self.session_name}")
            return True
        except Exception as e:
            print(f"Ошибка в сессии {self.session_name}: {str(e)}")
            return False
        finally:
            await self.client.stop()  # Гарантированное отключение


async def process_session(session_name: str):
    """Обработка одной сессии"""
    service = PyrogramService(session_name)
    if await service.start():
        # Здесь будут действия с аккаунтом
        # Например: отправка сообщений, сбор данных и т.д.
        pass


async def main_pyrogram():
    tdata_path = os.path.abspath("tdata")

    if not os.path.exists(tdata_path):
        print("Папка tdata не найдена!")
        return

    sessions = [
        entry for entry in os.listdir(tdata_path)
        if os.path.isdir(os.path.join(tdata_path, entry))
    ]

    if not sessions:
        print("Нет доступных сессий в tdata")
        return

    # Параллельный запуск всех сессий
    await asyncio.gather(*[process_session(session) for session in sessions])

# if __name__ == "__main__":
#     asyncio.run(main_pyrogram())