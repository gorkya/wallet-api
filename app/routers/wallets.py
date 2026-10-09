import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.database import get_session
from app.exceptions import WalletNotFoundError
from app.models import Wallet
from app.schemas import OperationRequest, WalletResponse

router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "", response_model=WalletResponse, status_code=status.HTTP_201_CREATED
)
async def create_wallet(session: SessionDep):
    wallet = await Wallet.create(session)
    await session.commit()
    return wallet


@router.get("/{wallet_id}", response_model=WalletResponse)
async def get_wallet(wallet_id: uuid.UUID, session: SessionDep):
    wallet = await Wallet.get_by_id(session, wallet_id)
    if wallet is None:
        raise WalletNotFoundError
    return wallet


@router.post("/{wallet_id}/operation", response_model=WalletResponse)
async def change_balance(
    wallet_id: uuid.UUID, body: OperationRequest, session: SessionDep
):
    balance = await services.change_balance(
        session, wallet_id, body.operation_type, body.amount
    )
    return WalletResponse(id=wallet_id, balance=balance)
