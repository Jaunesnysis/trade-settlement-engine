from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.break_record import BreakType


class BreakRecordResponse(BaseModel):
    id: UUID
    trade_ref: str
    break_type: BreakType
    internal_value: Optional[str]
    counterparty_value: Optional[str]
    description: str
    created_at: datetime

    class Config:
        from_attributes = True