from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.reconciliation_engine import run_reconciliation
from app.reports.csv_exporter import export_reconciliation_report

router = APIRouter(prefix="/reconciliation", tags=["Reconciliation"])


@router.post("/run")
def run(db: Session = Depends(get_db)):
    """Run full reconciliation pipeline — match trades, detect breaks, generate settlements."""
    result = run_reconciliation(db)
    return result


@router.post("/export")
def export(db: Session = Depends(get_db)):
    """Export reconciliation results to CSV report."""
    file_path = export_reconciliation_report(db)
    return {"file_path": file_path}