"""
    Авторизация с автоматическим созданием сессий
"""
import asyncio
import os
import logging
from pyrogram import Client, __version__
from pyrogram.errors import BadRequest, SessionPasswordNeeded
from settings import settings

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class PyrogramService:
    def __init__(self, session_name: str):
        self.session_name = session_name
        self.base_dir = os.path.abspath("tdata")
        os.makedirs(self.base_dir, exist_ok=True)
        self.session_path = os.path.join(self.base_dir, f"{session_name}.session")

        # Создаем пустую сессию, если её нет
        if not os.path.exists(self.session_path):
            logger.warning(f"Создаю новую сессию: {session_name}")
            with open(self.session_path, "w") as f:
                f.write("")

        self.client = Client(
            name=session_name,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            phone_number="+27837283875",
            workdir=self.base_dir,
            in_memory=False
        )

    async def start(self):
        try:
            await self.client.connect()

            if not await self.client.is_user_authorized():
                phone = input(f"Введите номер телефона для {self.session_name}: ")
                sent_code = await self.client.send_code(phone)

                code = input("Введите код из Telegram: ")
                try:
                    await self.client.sign_in(phone, sent_code.phone_code_hash, code)
                except SessionPasswordNeeded:
                    password = input("Введите пароль 2FA: ")
                    await self.client.check_password(password)

            me = await self.client.get_me()
            logger.info(f"Авторизован как: {me.first_name} (ID: {me.id})")
            return True

        except BadRequest as e:
            logger.error(f"Ошибка API: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            return False
        finally:
            if self.client.is_connected:
                await self.client.disconnect()

async def process_session(session_name: str):
    service = PyrogramService(session_name)
    return await service.start()

async def main_pyrogram():
    logger.info(f"Pyrogram v{__version__}")

    tdata_path = os.path.abspath("tdata")
    sessions = [
        os.path.splitext(f)[0]
        for f in os.listdir(tdata_path)
        if f.endswith(".session")
    ] or ["default_session"]  # Fallback

    await asyncio.gather(*[process_session(s) for s in sessions])

if __name__ == "__main__":
    asyncio.run(main_pyrogram())