from pyrogram import Client
from sqlalchemy.ext.asyncio import AsyncSession

from repository.repository_proxy import ProxyRepository
from service.session_service import logger


class ProxyService:
    def __init__(self, session: AsyncSession):
        self.repo = ProxyRepository(session)

    async def set_proxy(self, client: Client, proxy_id: int):
        """
        Устанавливаем прокси для клиента.
        """
        proxy = await self.repo.get_proxy_by_id(proxy_id)
        if not proxy:
            raise Exception("Прокси не найден")

        client.proxy = {
            "hostname": proxy.ip_address,
            "port": 1080,  # Это пример, укажи порт прокси
            "username": proxy.login,
            "password": proxy.password
        }
        logger.info(f"Прокси {proxy.ip_address} установлен для клиента")