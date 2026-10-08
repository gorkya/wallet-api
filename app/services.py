import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Wallet
from app.enums import OperationType
from app.exceptions import InsufficientFundsError, WalletNotFoundError


async def change_balance(
    session: AsyncSession,
    wallet_id: uuid.UUID,
    operation_type: OperationType,
    amount: Decimal,
) -> Decimal:
    new_balance = await Wallet.change_balance(
        session, wallet_id, operation_type, amount
    )

    if new_balance is None:
        wallet = await Wallet.get_by_id(session, wallet_id)
        await session.rollback()
        if wallet is None:
            raise WalletNotFoundError
        raise InsufficientFundsError

    await session.commit()
    return new_balance
