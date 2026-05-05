from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List
from .database import engine
from .repository import init_db, get_db, insert_assurance, get_latest_status, get_history
from .engine import evaluate_account, Observation
from .models import AssuranceLog
from .config import DEFAULT_MATERIALITY

app = FastAPI(title="Reality-Linked Accounting (RLA) API", version="2.0.0")

@app.on_event("startup")
def startup():
    init_db()

class ObservationInput(BaseModel):
    value: float
    trust: float = Field(ge=0.0, le=1.0, default=1.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AssuranceRequest(BaseModel):
    account_id: str
    claimed: float
    observations: List[ObservationInput]
    last_verified: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    materiality: float = Field(default=DEFAULT_MATERIALITY, gt=0)

@app.get("/accounts/{account_id}/status")
def get_status(account_id: str, db=Depends(get_db)):
    record = get_latest_status(db, account_id)
    if not record:
        raise HTTPException(status_code=404, detail="No assurance data found")
    return record

@app.get("/accounts/{account_id}/history")
def get_history_route(account_id: str, limit: int = 20, db=Depends(get_db)):
    return get_history(db, account_id, limit)

@app.post("/assure", status_code=201)
def submit_assurance(req: AssuranceRequest, db=Depends(get_db)):
    observations = [Observation(o.value, o.trust, o.timestamp) for o in req.observations]
    result = evaluate_account(req.claimed, observations, req.last_verified, req.materiality)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid observations")

    latest = get_latest_status(db, req.account_id)
    prev_hash = latest.id if latest else None

    ts = datetime.now(timezone.utc)
    record = AssuranceLog(
        id=AssuranceLog.generate_id(req.account_id, ts),
        account_id=req.account_id,
        claimed=req.claimed,
        observed=result.observed,
        relative_drift=result.relative_drift,
        confidence=result.confidence,
        risk=result.risk,
        source_trust=observations[-1].trust if observations else 0.0,
        prev_hash=prev_hash,
        created_at=ts
    )
    # Fix hash chain to use actual payload hash
    record.prev_hash = AssuranceLog.compute_hash(prev_hash, req.account_id, req.claimed, result.observed, ts) if not prev_hash else prev_hash

    return insert_assurance(db, record)
