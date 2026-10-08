import uuid
from decimal import Decimal

import pytest

from app import services
from app.enums import OperationType
from app.exceptions import InsufficientFundsError, WalletNotFoundError


async def test_new_wallet_has_zero_balance(wallet):
    assert wallet.balance == 0


async def test_deposit_increases_balance(session, wallet):
    balance = await services.change_balance(
        session, wallet.id, OperationType.DEPOSIT, Decimal("100.50")
    )

    assert balance == Decimal("100.50")


async def test_withdraw_decreases_balance(session, wallet):
    await services.change_balance(
        session, wallet.id, OperationType.DEPOSIT, Decimal("100")
    )

    balance = await services.change_balance(
        session, wallet.id, OperationType.WITHDRAW, Decimal("30")
    )

    assert balance == Decimal("70")


async def test_withdraw_more_than_balance_raises(session, wallet):
    await services.change_balance(
        session, wallet.id, OperationType.DEPOSIT, Decimal("10")
    )

    with pytest.raises(InsufficientFundsError):
        await services.change_balance(
            session, wallet.id, OperationType.WITHDRAW, Decimal("10.01")
        )


async def test_operation_on_unknown_wallet_raises(session):
    with pytest.raises(WalletNotFoundError):
        await services.change_balance(
            session, uuid.uuid4(), OperationType.DEPOSIT, Decimal("1")
        )
