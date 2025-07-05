from decimal import Decimal
from app.db.models import Wallet
from app.services.strategies.base import OperationStrategyAbstract


class WithDrawStrategy(OperationStrategyAbstract):
    """
    Strategy for handling withdraw operation on a wallet
    """
    def execute(self, wallet: Wallet, amount: Decimal) -> None:
        """
        Execute withdraw operation on the given wallet with the specified amount.
        Args:
            wallet (Wallet): The wallet instance on which the operation is performed.
            amount (float): The amount involved in the operation.
        """
        if amount < 1:
            raise ValueError("Amount must be greater than zero")
        wallet.withdraw(amount=amount)
