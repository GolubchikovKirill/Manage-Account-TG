import logging
from pyrogram import Client, errors
from repository.repository_accounts import RepositoryAccounts
from database.models import Accounts
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

logger = logging.getLogger(__name__)

class TelegramSessionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = RepositoryAccounts(session)

    async def create_client(self, account_id: int) -> Optional[Client]:
        """
        Создаёт и авторизует клиента Telegram.
        """
        # Получаем аккаунт из базы данных
        account = await self.repo.get_account_by_name(str(account_id))
        if not account:
            logger.error(f"Аккаунт с id {account_id} не найден")
            return None

        # Создаём экземпляр клиента Telegram
        client = Client(session_name=str(account.id), api_id="your_api_id", api_hash="your_api_hash")

        try:
            # Проверка на активность сессии, если сессия уже существует
            if await self._check_session(client):
                logger.info(f"Аккаунт {account.name} уже авторизован.")
                return client

            # Начинаем процесс авторизации
            await self._authorize_client(client, account)
            logger.info(f"Аккаунт {account.name} успешно авторизован.")
            return client

        except errors.FloodWait as e:
            logger.error(f"Таймаут при авторизации аккаунта {account.name}: {e}")
            return None
        except errors.PhoneCodeInvalid as e:
            logger.error(f"Неверный код для аккаунта {account.name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при авторизации аккаунта {account.name}: {e}")
            return None

    @staticmethod
    async def _check_session(client: Client) -> bool:
        """
        Проверяет, существует ли активная сессия для клиента.
        """
        try:
            me = await client.get_me()
            return me is not None
        except errors.FloodWait:
            return False
        except Exception:
            return False

    async def _authorize_client(self, client: Client, account: Accounts):
        """
        Авторизация клиента Telegram.
        """
        phone_number = account.phone_number

        try:
            await client.start(phone_number)
            # Подтверждение с кодом, если необходимо
            await client.send_code(phone_number)
        except errors.PhoneCodeInvalid as e:
            raise Exception(f"Ошибка при отправке кода для {account.name}: {e}")

        # Подтверждаем, что пользователь авторизован
        me = await client.get_me()
        if me is None:
            raise Exception(f"Не удалось получить данные пользователя для {account.name}")

        # Сохраняем состояние сессии в базе данных
        account.status = True  # Сессия активна
        self.session.add(account)
        await self.session.commit()

    async def get_client(self, account_id: int) -> Optional[Client]:
        """
        Получаем клиент для работы с Telegram по аккаунту.
        """
        account = await self.repo.get_account_by_name(str(account_id))
        if not account:
            logger.error(f"Аккаунт с id {account_id} не найден")
            return None

        # Создание клиента для работы с сессией
        client = Client(session_name=str(account.id), api_id="your_api_id", api_hash="your_api_hash")
        await client.start()  # Пробуем подключить клиента
        return client

    async def logout(self, account_id: int):
        """
        Логаут клиента (выход из аккаунта Telegram).
        """
        account = await self.repo.get_account_by_name(str(account_id))
        if not account:
            logger.error(f"Аккаунт с id {account_id} не найден")
            return

        # Создаём и подключаем клиента
        client = Client(session_name=str(account.id), api_id="your_api_id", api_hash="your_api_hash")
        await client.start()

        # Выход из аккаунта
        await client.stop()
        account.status = False  # Сессия деактивирована
        self.session.add(account)
        await self.session.commit()

        logger.info(f"Аккаунт {account.name} успешно разлогинен.")