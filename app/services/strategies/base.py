from abc import ABC, abstractmethod

from app.db.models import Wallet


class OperationStrategyAbstract(ABC):
    @abstractmethod
    def execute(self, wallet: Wallet, amount: float):
        pass
