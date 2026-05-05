from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.settlement import SettlementStatus


class SettlementResponse(BaseModel):
    id: UUID
    trade_ref: str
    internal_notional: Optional[float]
    counterparty_notional: Optional[float]
    currency: str
    settlement_date: datetime
    status: SettlementStatus
    created_at: datetime

    class Config:
        from_attributes = True