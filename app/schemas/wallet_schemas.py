from enum import Enum
from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, condecimal


class OperationType(Enum):
    """
    Enum representing the types of the wallet operations
    """
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletResponse(BaseModel):
    """
    Response model representing a wallet`s public data
    """
    wallet_id: str
    balance: Annotated[Decimal, condecimal(gt=0, max_digits=12, decimal_places=2)]


class BaseModelWallet(BaseModel):
    """
    Base model for wallet-related requests containing an amount field.
    The amount must be positive decimal with up to 12 digits and 2 decimal places.
    Extra fields are forbidden to avoid unexpected inputs.
    """
    model_config = {"extra": "forbid"}
    amount: Annotated[Decimal, condecimal(gt=0, max_digits=12, decimal_places=2)]


class OperationModel(BaseModelWallet):
    """
    Model representing a wallet operation request.
    Includes the operation types and an amount value.
    """
    operation_type: OperationType


class WalletCreateModel(BaseModelWallet):
    """
    Model for creating a new wallet with an initial amount value.
    """
    pass
