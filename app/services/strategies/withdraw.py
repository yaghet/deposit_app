from decimal import Decimal
from app.db.models import Wallet
from app.services.strategies.base import OperationStrategyAbstract


class WithDrawStrategy(OperationStrategyAbstract):
    def execute(self, wallet: Wallet, amount: Decimal) -> None:
        wallet.withdraw(amount=amount)
