from database.database import AsyncSession
from database.models import Accounts
from sqlalchemy import select


class RepositoryAccounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_account(
        self,
        name: str,
        last_name: str,
        status: bool = True,
        proxy_id: int | None = None
    ) -> Accounts:
        account = Accounts(name=name, last_name=last_name, status=status, session_data=proxy_id)
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def get_account_by_name(self, name: str) -> Accounts | None:
        result = await self.session.execute(select(Accounts).filter(Accounts.name == name))
        return result.scalars().first()

    async def delete_account(self, name: str) -> str:
        account = await self.get_account_by_name(name)
        if account:
            await self.session.delete(account)
            await self.session.commit()
            return f"Аккаунт '{account.name}' удалён"
        return f"Аккаунт '{name}' не найден"