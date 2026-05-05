from typing import Optional, List, Tuple
from app.models.trade import Trade
from app.models.break_record import BreakRecord, BreakType
import uuid


NOTIONAL_TOLERANCE = 0.01  # 1 cent tolerance for floating point


def detect_breaks(matched_pairs: List[Tuple]) -> List[BreakRecord]:
    """
    Analyses matched trade pairs and detects breaks.
    Returns list of BreakRecord objects to be saved to DB.
    """
    breaks = []

    for internal, counterparty in matched_pairs:

        # MISSING_TRADE — only on one side
        if internal is None:
            breaks.append(BreakRecord(
                id=uuid.uuid4(),
                trade_ref=counterparty.trade_ref,
                break_type=BreakType.MISSING_TRADE,
                internal_value=None,
                counterparty_value=counterparty.trade_ref,
                description=f"Trade {counterparty.trade_ref} exists on counterparty side but not internally"
            ))
            continue

        if counterparty is None:
            breaks.append(BreakRecord(
                id=uuid.uuid4(),
                trade_ref=internal.trade_ref,
                break_type=BreakType.MISSING_TRADE,
                internal_value=internal.trade_ref,
                counterparty_value=None,
                description=f"Trade {internal.trade_ref} exists internally but not on counterparty side"
            ))
            continue

        # NOTIONAL_MISMATCH
        if abs(internal.notional - counterparty.notional) > NOTIONAL_TOLERANCE:
            breaks.append(BreakRecord(
                id=uuid.uuid4(),
                trade_ref=internal.trade_ref,
                break_type=BreakType.NOTIONAL_MISMATCH,
                internal_value=str(internal.notional),
                counterparty_value=str(counterparty.notional),
                description=f"Notional mismatch: internal={internal.notional}, counterparty={counterparty.notional}"
            ))

        # DATE_MISMATCH
        if internal.settlement_date != counterparty.settlement_date:
            breaks.append(BreakRecord(
                id=uuid.uuid4(),
                trade_ref=internal.trade_ref,
                break_type=BreakType.DATE_MISMATCH,
                internal_value=str(internal.settlement_date),
                counterparty_value=str(counterparty.settlement_date),
                description=f"Settlement date mismatch: internal={internal.settlement_date}, counterparty={counterparty.settlement_date}"
            ))

        # CURRENCY_MISMATCH
        if internal.currency != counterparty.currency:
            breaks.append(BreakRecord(
                id=uuid.uuid4(),
                trade_ref=internal.trade_ref,
                break_type=BreakType.CURRENCY_MISMATCH,
                internal_value=internal.currency,
                counterparty_value=counterparty.currency,
                description=f"Currency mismatch: internal={internal.currency}, counterparty={counterparty.currency}"
            ))

    return breaks