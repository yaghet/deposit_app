import uuid
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Wallet(Base):

    """
    Database model represent a user`s wallet
    Attributes:
        uuid (str): Unique UUID of the wallet
        balance (Decimal): Current balance of the wallet, with precision up to 2 decimal places
    """

    __tablename__ = "wallets"

    uuid: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    def deposit(self, amount: Decimal) -> None:
        """
        Increases balance of the wallet by the specified amount
        Args:
            amount (Decimal): Amount to add to the balance (must be positive)
        """
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        """
        Decreases balance of the wallet by the specified amount.
        Args:
            amount (Decimal): Amound to subtrack from the balance (must be also positive)
        """
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def __repr__(self) -> str:
        return f'<Wallet(uuid="{self.uuid}", balance="{self.balance}")>'
