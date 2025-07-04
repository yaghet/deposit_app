from app.db.models import Wallet
from app.services.strategies.base import OperationStrategyAbstract


class WithDrawStrategy(OperationStrategyAbstract):
    def execute(self, wallet: Wallet, amount: float):
        wallet.withdraw(amount=amount)
