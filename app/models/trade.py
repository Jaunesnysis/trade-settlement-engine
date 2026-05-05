from sqlalchemy import Column, String, Float, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum
from datetime import datetime


class TradeSource(str, enum.Enum):
    INTERNAL = "INTERNAL"
    COUNTERPARTY = "COUNTERPARTY"


class InstrumentType(str, enum.Enum):
    FX_SPOT = "FX_SPOT"
    FX_FORWARD = "FX_FORWARD"
    INTEREST_RATE_SWAP = "INTEREST_RATE_SWAP"
    BOND = "BOND"
    EQUITY = "EQUITY"


class Trade(Base):
    __tablename__ = "trades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_ref = Column(String, nullable=False)
    source = Column(SAEnum(TradeSource), nullable=False)         # INTERNAL or COUNTERPARTY
    instrument_type = Column(SAEnum(InstrumentType), nullable=False)
    notional = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    trade_date = Column(DateTime, nullable=False)
    settlement_date = Column(DateTime, nullable=False)
    counterparty_lei = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)