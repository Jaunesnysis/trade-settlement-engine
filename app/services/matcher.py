from typing import Optional, Tuple, List
from app.models.trade import Trade, TradeSource


def find_match(internal_trade: Trade, counterparty_trades: List[Trade]) -> Optional[Trade]:
    """
    Tries to find a matching counterparty trade for an internal trade.
    Match is based on trade_ref and currency.
    """
    for cp_trade in counterparty_trades:
        if cp_trade.trade_ref == internal_trade.trade_ref and \
           cp_trade.currency == internal_trade.currency:
            return cp_trade
    return None


def match_trades(internal_trades: List[Trade], counterparty_trades: List[Trade]) -> List[Tuple]:
    """
    Matches internal trades against counterparty trades.
    Returns list of tuples: (internal_trade, counterparty_trade or None)
    """
    matched = []
    matched_cp_refs = set()

    for internal in internal_trades:
        match = find_match(internal, counterparty_trades)
        if match:
            matched.append((internal, match))
            matched_cp_refs.add(match.trade_ref)
        else:
            matched.append((internal, None))

    # Find counterparty trades with no internal match
    for cp in counterparty_trades:
        if cp.trade_ref not in matched_cp_refs:
            matched.append((None, cp))

    return matched