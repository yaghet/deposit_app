from app.db.models import Wallet
from app.services.strategies.base import OperationStrategyAbstract


class DepositStrategy(OperationStrategyAbstract):
    def execute(self, wallet: Wallet, amount: float):
        wallet.deposit(amount=amount)
