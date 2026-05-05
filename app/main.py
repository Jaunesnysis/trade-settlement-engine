from fastapi import FastAPI
from app.routers import trades, settlements, reconciliation, health
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trade Settlement & Reconciliation Engine",
    description="Post-trade settlement matching and break detection pipeline",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(trades.router)
app.include_router(settlements.router)
app.include_router(reconciliation.router)