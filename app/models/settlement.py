from sqlalchemy import Column, String, Float, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum
from datetime import datetime


class SettlementStatus(str, enum.Enum):
    PENDING = "PENDING"
    MATCHED = "MATCHED"
    BROKEN = "BROKEN"
    SETTLED = "SETTLED"


class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_ref = Column(String, nullable=False)
    internal_notional = Column(Float, nullable=True)
    counterparty_notional = Column(Float, nullable=True)
    currency = Column(String(3), nullable=False)
    settlement_date = Column(DateTime, nullable=False)
    status = Column(SAEnum(SettlementStatus), default=SettlementStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)