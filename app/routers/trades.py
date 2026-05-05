from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeResponse
from typing import List
import uuid

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.post("/", response_model=TradeResponse)
def submit_trade(trade_in: TradeCreate, db: Session = Depends(get_db)):
    trade = Trade(id=uuid.uuid4(), **trade_in.model_dump())
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade


@router.get("/", response_model=List[TradeResponse])
def get_trades(db: Session = Depends(get_db)):
    return db.query(Trade).all()