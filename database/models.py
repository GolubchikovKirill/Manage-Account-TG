from sqlalchemy import Boolean, ForeignKey, Text
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Accounts(Base):
    __tablename__ = "Accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    status: Mapped[bool] = mapped_column(Boolean)
    name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    session_data: Mapped[int] = mapped_column(ForeignKey("Proxy.id"), index=True)


class Proxy(Base):
    __tablename__ = "Proxy"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ip_address: Mapped[str] = mapped_column(index=True, unique=True)
    login: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column(index=True, unique=True)

    # Один ко многим
    accounts: Mapped[list["Accounts"]] = relationship("Accounts", backref="proxy")


class Channels(Base):
    __tablename__ = "Channels"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("Accounts.id"), index=True)
    comment: Mapped[str] = mapped_column(Text)

    account: Mapped["Accounts"] = relationship("Accounts", backref="сhannels")
