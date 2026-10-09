import asyncio
from decimal import Decimal

from app import services
from app.enums import OperationType
from app.exceptions import InsufficientFundsError
from app.models import Wallet


async def _operation(session_maker, wallet_id, operation_type, amount):
    async with session_maker() as session:
        return await services.change_balance(
            session, wallet_id, operation_type, Decimal(amount)
        )


async def _get_balance(session_maker, wallet_id):
    async with session_maker() as session:
        wallet = await Wallet.get_by_id(session, wallet_id)
        return wallet.balance


async def test_concurrent_deposits_are_not_lost(session_maker, wallet):
    tasks = [
        _operation(session_maker, wallet.id, OperationType.DEPOSIT, "10")
        for _ in range(100)
    ]

    await asyncio.gather(*tasks)

    assert await _get_balance(session_maker, wallet.id) == Decimal("1000")


async def test_concurrent_withdrawals_never_overdraw(session_maker, wallet):
    await _operation(session_maker, wallet.id, OperationType.DEPOSIT, "100")

    tasks = [
        _operation(session_maker, wallet.id, OperationType.WITHDRAW, "10")
        for _ in range(30)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    succeeded = [r for r in results if isinstance(r, Decimal)]
    rejected = [r for r in results if isinstance(r, InsufficientFundsError)]

    assert len(succeeded) == 10
    assert len(rejected) == 20
    assert await _get_balance(session_maker, wallet.id) == Decimal("0")
