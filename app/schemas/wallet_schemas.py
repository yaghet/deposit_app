from enum import Enum

from pydantic import BaseModel, condecimal


class OperationType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletResponse(BaseModel):
    wallet_id: str
    balance: condecimal(max_digits=12, decimal_places=2)


class BaseModelWallet(BaseModel):
    model_config = {"extra": "forbid"}
    amount: condecimal(gt=0, max_digits=12, decimal_places=2)


class OperationModel(BaseModelWallet):
    operation_type: OperationType


class WalletCreateModel(BaseModelWallet):
    pass
