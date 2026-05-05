import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.settlement import Settlement
from app.models.break_record import BreakRecord


REPORTS_DIR = "reports_output"


def export_reconciliation_report(db: Session) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_name = f"RECON-{timestamp}.csv"
    file_path = os.path.join(REPORTS_DIR, file_name)

    settlements = db.query(Settlement).all()
    breaks = db.query(BreakRecord).all()
    breaks_by_ref = {}
    for b in breaks:
        breaks_by_ref.setdefault(b.trade_ref, []).append(b)

    with open(file_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "trade_ref",
            "internal_notional",
            "counterparty_notional",
            "currency",
            "settlement_date",
            "status",
            "break_type",
            "break_description",
        ])

        for s in settlements:
            trade_breaks = breaks_by_ref.get(s.trade_ref, [])
            if trade_breaks:
                for b in trade_breaks:
                    writer.writerow([
                        s.trade_ref,
                        s.internal_notional,
                        s.counterparty_notional,
                        s.currency,
                        s.settlement_date.strftime("%Y-%m-%d"),
                        s.status.value,
                        b.break_type.value,
                        b.description,
                    ])
            else:
                writer.writerow([
                    s.trade_ref,
                    s.internal_notional,
                    s.counterparty_notional,
                    s.currency,
                    s.settlement_date.strftime("%Y-%m-%d"),
                    s.status.value,
                    "",
                    "",
                ])

    return file_path