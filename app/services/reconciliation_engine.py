from sqlalchemy.orm import Session
from app.models.trade import Trade, TradeSource
from app.models.settlement import Settlement, SettlementStatus
from app.models.break_record import BreakRecord
from app.services.matcher import match_trades
from app.services.break_detector import detect_breaks
import uuid
from datetime import datetime


def run_reconciliation(db: Session) -> dict:
    """
    Full reconciliation pipeline:
    1. Fetch internal and counterparty trades
    2. Match them
    3. Detect breaks
    4. Create settlement records
    5. Save break records
    """

    internal_trades = db.query(Trade).filter(
        Trade.source == TradeSource.INTERNAL
    ).all()

    counterparty_trades = db.query(Trade).filter(
        Trade.source == TradeSource.COUNTERPARTY
    ).all()

    matched_pairs = match_trades(internal_trades, counterparty_trades)
    breaks = detect_breaks(matched_pairs)

    settlements = []
    for internal, counterparty in matched_pairs:
        trade_ref = internal.trade_ref if internal else counterparty.trade_ref
        currency = internal.currency if internal else counterparty.currency
        settlement_date = internal.settlement_date if internal else counterparty.settlement_date

        has_break = any(b.trade_ref == trade_ref for b in breaks)

        settlement = Settlement(
            id=uuid.uuid4(),
            trade_ref=trade_ref,
            internal_notional=internal.notional if internal else None,
            counterparty_notional=counterparty.notional if counterparty else None,
            currency=currency,
            settlement_date=settlement_date,
            status=SettlementStatus.BROKEN if has_break else SettlementStatus.MATCHED,
        )
        settlements.append(settlement)

    for s in settlements:
        db.add(s)
    for b in breaks:
        db.add(b)

    db.commit()

    return {
        "total_trades": len(matched_pairs),
        "matched": sum(1 for s in settlements if s.status == SettlementStatus.MATCHED),
        "broken": sum(1 for s in settlements if s.status == SettlementStatus.BROKEN),
        "breaks_detected": len(breaks),
    }