from decimal import Decimal

from abc import ABC, abstractmethod

from app.db.models import Wallet


class OperationStrategyAbstract(ABC):
    """
    Abstract base class for operation strategies on a Wallet.

    Subclasses must implement the execute method to define
    specific operations involving a Wallet and an amount.
    """
    @abstractmethod
    def execute(self, wallet: Wallet, amount: Decimal) -> None:
        """
        Execute the operation on the given wallet with the specified amount.
        Args:
            wallet (Wallet): The wallet instance on which the operation is performed.
            amount (float): The amount involved in the operation.
        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        pass
