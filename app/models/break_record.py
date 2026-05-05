from sqlalchemy import Column, String, Float, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum
from datetime import datetime


class BreakType(str, enum.Enum):
    NOTIONAL_MISMATCH = "NOTIONAL_MISMATCH"
    MISSING_TRADE = "MISSING_TRADE"
    DATE_MISMATCH = "DATE_MISMATCH"
    CURRENCY_MISMATCH = "CURRENCY_MISMATCH"


class BreakRecord(Base):
    __tablename__ = "break_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_ref = Column(String, nullable=False)
    break_type = Column(SAEnum(BreakType), nullable=False)
    internal_value = Column(String, nullable=True)
    counterparty_value = Column(String, nullable=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)