import uuid
from decimal import Decimal

from pydantic import BaseModel, Field

from app.enums import OperationType


class OperationRequest(BaseModel):
    operation_type: OperationType
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)


class WalletResponse(BaseModel):
    id: uuid.UUID
    balance: Decimal
