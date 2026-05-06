from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
import hashlib
import json

Base = declarative_base()


class AssuranceLog(Base):
    """Append-only ledger with cryptographic chaining."""
    __tablename__ = "assurance_log"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, nullable=False, index=True)

    claimed = Column(Float, nullable=False)
    observed = Column(Float, nullable=False)
    relative_drift = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    risk = Column(Float, nullable=False)
    source_trust = Column(Float, nullable=False)

    prev_hash = Column(Text, nullable=True)
    hash = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    # -----------------------------
    # ID Generation
    # -----------------------------
    @staticmethod
    def generate_id(account_id: str, ts: datetime) -> str:
        return f"{account_id}_{int(ts.timestamp())}"


    # -----------------------------
    # Secure Hashing (FIXED)
    # -----------------------------
    @staticmethod
    def compute_hash(
        prev_hash: str | None,
        account_id: str,
        claimed: float,
        observed: float,
        drift: float,
        confidence: float,
        risk: float,
        ts: datetime,
    ) -> str:
        payload = {
            "prev_hash": prev_hash,
            "account_id": account_id,
            "claimed": round(claimed, 6),
            "observed": round(observed, 6),
            "drift": round(drift, 6),
            "confidence": round(confidence, 6),
            "risk": round(risk, 6),
            "timestamp": ts.isoformat(),
        }

        encoded = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()
