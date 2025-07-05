import uuid
import logging
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.db.models import Wallet
from app.schemas.wallet_schemas import OperationModel
from app.services.strategies.base import OperationStrategyAbstract
from app.services.strategies.deposit import DepositStrategy
from app.services.strategies.withdraw import WithDrawStrategy
from app.exceptions import WalletNotFoundException, OperationExecutionException, InvalidOperationException

logger = logging.getLogger(__name__)


class WalletService:
    """
    Service for managing user`s wallets
        Provides methods to create a wallet, retrieve wallet information
        and perform balance operations like (deposit or withdraw)
    Attributes:
        session AsyncSession: Asynchronous SQLAlchemy session for database operations.
        _strategies (dict): Dictionary of operation strategies keyed by operation type.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the service with a database session and set up operation strategies.
        Args:
            session AsyncSession: Asynchronous session for database access
        """
        self.session = session
        self._strategies: dict[str, OperationStrategyAbstract] = {
            "DEPOSIT": DepositStrategy(),
            "WITHDRAW": WithDrawStrategy(),
        }

    async def get_wallet(self, wallet_id: str) -> Wallet:
        """
        Retrieve a wallet by its UUID
        Locks the record for update to prevent race conditions during balance changes.
        Args:
            wallet_id (str): UUID of the wallet
        Returns:
            Wallet: Wallet object from the database
        """
        logger.debug(f'Fetching wallet with ID {wallet_id}')
        try:
            result = await self.session.execute(
                select(Wallet)
                .where(Wallet.uuid == wallet_id)
                .with_for_update()
            )
            wallet = result.scalar_one_or_none()
            if not wallet:
                logger.warning(f'Wallet with {wallet_id} not found')
                raise WalletNotFoundException()
            logger.debug(f'Wallet found {wallet_id}')
            return wallet
        except Exception as e:
            logger.error(f'Error fetching wallet {wallet_id}: {e}')
            raise

    async def perform_wallet(self, wallet_id: str, operation: OperationModel) -> Wallet:
        """
        Perform an operation on wallet like (deposit or withdraw)
        Uses the strategy pattern to select the execution algorithm
        Args:
            wallet_id (str): UUID of the wallet
            operation (OperationModel): Operation model containing type and amount
        Returns:
            Wallet: Updated wallet object after the operation
        """
        logger.debug(
            f'Forming operation {operation.operation_type.value} on wallet {wallet_id} with amount {operation.amount}')
        try:
            async with self.session.begin():
                wallet = await self.get_wallet(wallet_id=wallet_id)
                strategy = self._strategies.get(operation.operation_type.value)

                if not strategy:
                    logger.error(f'Invalid operation type {operation.operation_type.value}')
                    raise InvalidOperationException()

                try:
                    strategy.execute(wallet, operation.amount)
                    logger.info(
                        f'Operation {operation.operation_type.value} executed successfully on wallet {wallet_id}')
                except ValueError as exp:
                    logger.error(f'Operation execution failed {str(exp)}')
                    raise OperationExecutionException(detail=str(exp))

                self.session.add(wallet)

            await self.session.refresh(wallet)

            return wallet

        except IntegrityError as exp:
            await self.session.rollback()
            logger.error(f'Integrity error during executing operation {exp.orig}')
            raise HTTPException(status_code=400, detail='Data integrity violation')
        except Exception as exp:
            await self.session.rollback()
            logger.error(f'Unexpected error during wallet operation {exp}')
            raise HTTPException(status_code=500, detail='Internal Server Error')

    async def create_wallet(self, amount: Decimal) -> Wallet:
        """
        Create a new wallet with an initial balance
        Generates unique UUID of the wallet
        Args:
            amount (Decimal): Initial wallet balance (should be non-negative)
        Returns:
            Wallet: Just created wallet object
        """
        wallet_uuid = str(uuid.uuid4())
        new_wallet = Wallet(uuid=wallet_uuid, balance=amount)
        logger.info(f'Creating a new wallet with ID {wallet_uuid} and initial balance {amount}')
        try:
            self.session.add(new_wallet)

            await self.session.commit()
            await self.session.refresh(new_wallet)
        except IntegrityError as exp:
            await self.session.rollback()
            logger.error(f'Integrity error during executing operation {exp.orig}')
            raise HTTPException(status_code=400, detail='Data integrity violation')
        except Exception as exp:
            await self.session.rollback()
            logger.error(f'Unexpected error during wallet operation {exp}')
            raise HTTPException(status_code=500, detail='Internal Server Error')

        logger.info(f'Wallet created successfully with ID {wallet_uuid}')
        return new_wallet
