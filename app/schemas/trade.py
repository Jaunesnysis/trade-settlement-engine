from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.trade import InstrumentType, TradeSource


class TradeCreate(BaseModel):
    trade_ref: str = Field(..., example="TRD-20240501-001")
    source: TradeSource
    instrument_type: InstrumentType
    notional: float = Field(..., gt=0, example=1500000.0)
    currency: str = Field(..., min_length=3, max_length=3, example="EUR")
    trade_date: datetime
    settlement_date: datetime
    counterparty_lei: str = Field(..., min_length=20, max_length=20, example="SWEDSESS00LEI000001X")


class TradeResponse(BaseModel):
    id: UUID
    trade_ref: str
    source: TradeSource
    instrument_type: InstrumentType
    notional: float
    currency: str
    trade_date: datetime
    settlement_date: datetime
    counterparty_lei: str
    created_at: datetime

    class Config:
        from_attributes = True