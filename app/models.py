import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, update
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.enums import OperationType


class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = (
        CheckConstraint("balance >= 0", name="ck_wallets_balance_non_negative"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=0, server_default="0"
    )

    @classmethod
    async def change_balance(
        cls,
        session: AsyncSession,
        wallet_id: uuid.UUID,
        operation_type: OperationType,
        amount: Decimal,
    ) -> Decimal | None:
        """Атомарно меняет баланс одним UPDATE.

        Возвращает новый баланс или None, если строка не обновилась:
        кошелька нет или не хватает средств при WITHDRAW.
        """
        stmt = update(cls).where(cls.id == wallet_id)
        if operation_type is OperationType.DEPOSIT:
            stmt = stmt.values(balance=cls.balance + amount)
        else:
            stmt = stmt.where(cls.balance >= amount).values(
                balance=cls.balance - amount
            )
        return await session.scalar(stmt.returning(cls.balance))
