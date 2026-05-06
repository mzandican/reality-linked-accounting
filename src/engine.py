"""Reality-Linked Accounting: Confidence & Aggregation Engine (Stable)."""
import math
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from .config import EPSILON, DECAY_LAMBDA, DRIFT_PENALTY_K, DEFAULT_MATERIALITY


# -----------------------------
# Data Structures
# -----------------------------

@dataclass
class Observation:
    value: float
    trust: float
    timestamp: datetime


@dataclass
class AssuranceResult:
    claimed: float
    observed: float
    relative_drift: float
    confidence: float
    risk: float


# -----------------------------
# Confidence Function
# -----------------------------

def compute_confidence(
    drift: float,
    age_seconds: float,
    lambda_decay: float = DECAY_LAMBDA,
    k_drift: float = DRIFT_PENALTY_K,
) -> float:
    """
    C = exp(-λt) * exp(-k·drift)
    Always bounded in [0,1]
    """

    drift = max(0.0, float(drift))
    age_seconds = max(0.0, float(age_seconds))

    # Prevent underflow
    decay_exp = max(-lambda_decay * age_seconds, -700)
    drift_exp = max(-k_drift * drift, -700)

    confidence = math.exp(decay_exp) * math.exp(drift_exp)

    return max(0.0, min(1.0, confidence))


# -----------------------------
# Robust Aggregation (FIXED)
# -----------------------------

def aggregate_observations(
    observations: List[Observation],
    now: Optional[datetime] = None
) -> float:
    """
    Robust aggregation using:
    - trust weighting (squared for stronger penalty)
    - recency decay
    - weighted mean (no distortion)
    """

    if not observations:
        return 0.0

    now = now or datetime.utcnow()

    weighted_sum = 0.0
    total_weight = 0.0

    for obs in observations:
        if obs is None:
            continue

        # Clamp trust
        trust = min(max(obs.trust, 0.0), 1.0)

        # Stronger penalty on low trust
        trust_weight = trust ** 2

        # Handle time safely
        age = (now - obs.timestamp).total_seconds()
        age = max(0.0, age)

        decay_exp = max(-DECAY_LAMBDA * age, -700)
        recency_weight = math.exp(decay_exp)

        weight = trust_weight * recency_weight

        if weight <= 0.0:
            continue

        weighted_sum += obs.value * weight
        total_weight += weight

    if total_weight <= EPSILON:
        return 0.0

    return weighted_sum / total_weight


# -----------------------------
# Full Evaluation Pipeline
# -----------------------------

def evaluate_account(
    claimed: float,
    observations: List[Observation],
    last_verified: datetime,
    materiality: float = DEFAULT_MATERIALITY,
    now: Optional[datetime] = None
) -> Optional[AssuranceResult]:

    now = now or datetime.utcnow()

    observed = aggregate_observations(observations, now=now)

    denominator = max(abs(claimed), EPSILON)
    relative_drift = abs(claimed - observed) / denominator

    age = (now - last_verified).total_seconds()
    age = max(0.0, age)

    confidence = compute_confidence(relative_drift, age)

    risk = relative_drift * (1.0 - confidence) * max(materiality, 0.0)

    return AssuranceResult(
        claimed=claimed,
        observed=observed,
        relative_drift=relative_drift,
        confidence=confidence,
        risk=risk,
)
