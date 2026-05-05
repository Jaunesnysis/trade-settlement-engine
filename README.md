# Trade Settlement & Reconciliation Engine

A backend API simulating a **post-trade settlement and reconciliation pipeline**, modelled after real-world workflows used by banks and financial institutions across Europe.

Built with **Python**, **FastAPI**, and **PostgreSQL**.

---

## What It Does

After a trade is executed, both sides of the transaction (internal desk and counterparty) must independently confirm and settle it. This system simulates that process — ingesting trades from both sides, matching them, detecting discrepancies, and generating reconciliation reports.

1. **Trade Ingestion** — accepts trades from both INTERNAL and COUNTERPARTY sources
2. **Matching** — pairs internal trades against counterparty trades by reference and currency
3. **Break Detection** — identifies discrepancies between matched pairs
4. **Settlement Records** — creates a settlement record for every trade pair with MATCHED or BROKEN status
5. **Reconciliation Report** — exports full results to CSV for operations teams

---

## Break Types Detected

| Break Type          | Description                               |
| ------------------- | ----------------------------------------- |
| `NOTIONAL_MISMATCH` | Both sides report different trade amounts |
| `MISSING_TRADE`     | Trade exists on one side only             |
| `DATE_MISMATCH`     | Settlement dates do not agree             |
| `CURRENCY_MISMATCH` | Currencies do not match                   |

---

## Tech Stack

| Layer          | Technology    |
| -------------- | ------------- |
| API            | FastAPI       |
| Database       | PostgreSQL 15 |
| ORM            | SQLAlchemy    |
| Validation     | Pydantic v2   |
| Infrastructure | Docker        |
| Language       | Python 3.9+   |

---

## Project Structure

app/
├── models/ # SQLAlchemy ORM models (Trade, Settlement, BreakRecord)
├── schemas/ # Pydantic request/response schemas
├── routers/ # FastAPI endpoints
├── services/ # Business logic (matcher, break detector, reconciliation engine)
└── reports/ # CSV exporter

---

## Getting Started

### Prerequisites

- Docker
- Python 3.9+

### Run locally

```bash
# Start PostgreSQL
docker-compose up -d

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint                 | Description                               |
| ------ | ------------------------ | ----------------------------------------- |
| GET    | `/health`                | Service health check                      |
| POST   | `/trades/`               | Submit a trade (internal or counterparty) |
| GET    | `/trades/`               | Get all submitted trades                  |
| GET    | `/settlements/`          | Get all settlement records                |
| POST   | `/reconciliation/run`    | Run full reconciliation pipeline          |
| POST   | `/reconciliation/export` | Export reconciliation results to CSV      |

---

## Example Workflow

### 1. Submit internal trade

```json
{
  "trade_ref": "TRD-20240501-001",
  "source": "INTERNAL",
  "instrument_type": "FX_SPOT",
  "notional": 1500000.0,
  "currency": "EUR",
  "trade_date": "2024-05-01T10:00:00",
  "settlement_date": "2024-05-03T10:00:00",
  "counterparty_lei": "SWEDSESS00LEI000001X"
}
```

### 2. Submit counterparty trade (with notional mismatch)

```json
{
  "trade_ref": "TRD-20240501-001",
  "source": "COUNTERPARTY",
  "instrument_type": "FX_SPOT",
  "notional": 1499000.0,
  "currency": "EUR",
  "trade_date": "2024-05-01T10:00:00",
  "settlement_date": "2024-05-03T10:00:00",
  "counterparty_lei": "SWEDSESS00LEI000001X"
}
```

### 3. Run reconciliation

POST /reconciliation/run

### 4. Response

```json
{
  "total_trades": 3,
  "matched": 0,
  "broken": 3,
  "breaks_detected": 3
}
```

### 5. Generated CSV report

trade_ref,internal_notional,counterparty_notional,currency,settlement_date,status,break_type,break_description
TRD-20240501-001,1500000.0,1499000.0,EUR,2024-05-03,BROKEN,NOTIONAL_MISMATCH,"Notional mismatch: internal=1500000.0, counterparty=1499000.0"
TRD-20240501-002,2000000.0,,EUR,2024-05-03,BROKEN,MISSING_TRADE,Trade TRD-20240501-002 exists internally but not on counterparty side
TRD-20240501-003,,500000.0,USD,2024-05-04,BROKEN,MISSING_TRADE,Trade TRD-20240501-003 exists on counterparty side but not internally
