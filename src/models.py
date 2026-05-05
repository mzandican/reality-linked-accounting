from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
import hashlib

Base = declarative_base()

class AssuranceLog(Base):
    """Append-only ledger. Never updated. Cryptographically chained."""
    __tablename__ = "assurance_log"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, nullable=False, index=True)
    claimed = Column(Float, nullable=False)
    observed = Column(Float, nullable=False)
    relative_drift = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    risk = Column(Float, nullable=False)
    source_trust = Column(Float, nullable=False)
    prev_hash = Column(Text, nullable=True)  # Chain integrity
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def generate_id(account_id: str, ts: datetime) -> str:
        return f"{account_id}_{int(ts.timestamp())}"

    @staticmethod
    def compute_hash(prev_hash: str | None, account_id: str, claimed: float, observed: float, ts: datetime) -> str:
        payload = f"{prev_hash or ''}{account_id}{claimed}{observed}{ts.isoformat()}"
        return hashlib.sha256(payload.encode()).hexdigest()
