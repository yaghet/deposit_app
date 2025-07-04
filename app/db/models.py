import uuid
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = "wallets"

    uuid: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    def deposit(self, amount: Decimal) -> None:
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def __repr__(self) -> str:
        return f'<Wallet(uuid="{self.uuid}", balance="{self.balance}")>'
