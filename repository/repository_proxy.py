from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Proxy


class ProxyRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_proxy(self, ip_address: str, login: str, password: str) -> Proxy:
        proxy = Proxy(ip_address=ip_address, login=login, password=password)
        self.session.add(proxy)
        await self.session.commit()
        await self.session.refresh(proxy)
        return proxy

    async def get_proxy_by_ip(self, ip_address: str) -> Proxy | None:
        result = await self.session.execute(
            select(Proxy).filter(Proxy.ip_address == ip_address)
        )
        return result.scalars().first()

    async def delete_proxy(self, ip_address: str) -> str:
        proxy = await self.get_proxy_by_ip(ip_address)
        if proxy:
            await self.session.delete(proxy)
            await self.session.commit()
            return f"Прокси {proxy.ip_address} удалён"
        return f"Прокси {ip_address} не найден"