from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.settlement import Settlement
from app.schemas.settlement import SettlementResponse
from typing import List

router = APIRouter(prefix="/settlements", tags=["Settlements"])


@router.get("/", response_model=List[SettlementResponse])
def get_settlements(db: Session = Depends(get_db)):
    return db.query(Settlement).all()