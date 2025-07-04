from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.wallet_schemas import OperationModel, WalletResponse, WalletCreateModel
from app.services.wallet_service import WalletService

router = APIRouter(
    prefix="/api/v1/wallets",
    tags=["wallets"],
)

WalletID = Annotated[str, Path(title="Wallet ID")]
Session: AsyncSession = Depends(get_session)


@router.post(
    "/",
    response_model=WalletResponse,
    summary="Create a new wallet",
    description="Create a new wallet with an initial balance.",
)
async def create_wallet(
    wallet_create: Annotated[
        WalletCreateModel,
        Body(
            examples={
                "normal": {
                    "summary": "Normal example",
                    "description": "Create wallet with initial amount",
                    "value": {"amount": 100.00},
                },
                "invalid": {
                    "summary": "Invalid example",
                    "description": "Negative amount is invalid",
                    "value": {"amount": -10.00},
                },
            },
        ),
    ],
    session: AsyncSession = Depends(get_session),
):
    """Create a new wallet with a specified initial amount"""

    service = WalletService(session)
    wallet = await service.create_wallet(wallet_create.amount)
    return WalletResponse(wallet_id=wallet.uuid, balance=wallet.balance)


@router.post(
    "/{wallet_id}/operation",
    response_model=WalletResponse,
    summary="Perform wallet operation",
    description="Deposit or withdraw an amount from the wallet.",
)
async def create_deposit(
    wallet_id: WalletID,
    operation: Annotated[
        OperationModel,
        Body(
            examples={
                "deposit": {
                    "summary": "Deposit example",
                    "description": "Deposit 50.00 to wallet",
                    "value": {"operation_type": "DEPOSIT", "amount": 50.00},
                },
                "withdraw": {
                    "summary": "Withdraw example",
                    "description": "Withdraw 20.00 from wallet",
                    "value": {"operation_type": "WITHDRAW", "amount": 20.00},
                },
            },
        ),
    ],
    session: AsyncSession = Depends(get_session),
):
    """Performs a deposit or withdrawal operation on the specified wallet."""
    service = WalletService(session)
    wallet = await service.perform_wallet(wallet_id, operation)

    return WalletResponse(wallet_id=wallet.uuid, balance=wallet.balance)


@router.get(
    "/{wallet_id}/balance",
    response_model=WalletResponse,
    summary="Get wallet balance",
    description="Retrieve the current balance of the specified wallet by uuid.",
)
async def get_balance_by_uuid(
    wallet_id: WalletID,
    session: AsyncSession = Depends(get_session),
):
    """Returns the current balance for the wallet identified by `wallet_id`."""
    service = WalletService(session)
    wallet = await service.get_wallet(wallet_id)

    return WalletResponse(wallet_id=wallet.uuid, balance=wallet.balance)
