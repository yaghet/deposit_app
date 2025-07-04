import uuid
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Wallet
from app.schemas.wallet_schemas import OperationModel
from app.services.strategies.base import OperationStrategyAbstract
from app.services.strategies.deposit import DepositStrategy
from app.services.strategies.withdraw import WithDrawStrategy


class WalletService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._strategies: dict[str, OperationStrategyAbstract] = {
            "DEPOSIT": DepositStrategy(),
            "WITHDRAW": WithDrawStrategy(),
        }

    async def get_wallet(self, wallet_id: str) -> Wallet:
        result = await self.session.execute(
            select(Wallet)
            .where(Wallet.uuid == wallet_id)
            .with_for_update()
        )
        wallet = result.scalar_one_or_none()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet Not Found")
        return wallet

    async def perform_wallet(self, wallet_id: str, operation: OperationModel) -> Wallet:
        async with self.session.begin():
            wallet = await self.get_wallet(wallet_id=wallet_id)
            strategy = self._strategies.get(operation.operation_type.value)

            if not strategy:
                raise HTTPException(status_code=400, detail="Invalid Operation Type")

            try:
                strategy.execute(wallet, operation.amount)
            except ValueError as exp:
                raise HTTPException(status_code=400, detail=str(exp))

            self.session.add(wallet)

        await self.session.refresh(wallet)

        return wallet

    async def create_wallet(self, amount: Decimal) -> Wallet:
        wallet_uuid = str(uuid.uuid4())
        new_wallet = Wallet(uuid=wallet_uuid, balance=amount)

        self.session.add(new_wallet)

        await self.session.commit()
        await self.session.refresh(new_wallet)

        return new_wallet
