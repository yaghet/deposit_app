from decimal import Decimal
from app.db.models import Wallet
from app.services.strategies.base import OperationStrategyAbstract


class DepositStrategy(OperationStrategyAbstract):
    """
    Strategy for handling operation deposit on a wallet
    """
    def execute(self, wallet: Wallet, amount: Decimal) -> None:
        """
        Execute a deposit on the given wallet with the specified amount.
        Args:
            wallet (Wallet): The wallet instance on which the operation is performed.
            amount (float): The amount involved in the operation.
        """
        if amount < 1:
            raise ValueError("Amount must be greater than zero")
        wallet.deposit(amount=amount)
