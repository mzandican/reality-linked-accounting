"""Reality-Linked Accounting: Confidence & Aggregation Engine (Hardened)."""
import math
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from .config import EPSILON, DECAY_LAMBDA, DRIFT_PENALTY_K, DEFAULT_MATERIALITY


# ---- Data Structures ----

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


# ---- Core Math ----

def compute_confidence(
    drift: float,
    age_seconds: float,
    lambda_decay: float = DECAY_LAMBDA,
    k_drift: float = DRIFT_PENALTY_K,
) -> float:
    """
    Stable confidence computation:
    C = e^(-λt) * e^(-k·d_r)
    """

    # Sanitize inputs
    drift = max(0.0, float(drift))
    age_seconds = max(0.0, float(age_seconds))

    # Prevent overflow / underflow extremes
    decay_exponent = -lambda_decay * age_seconds
    drift_exponent = -k_drift * drift

    # Clamp exponents to safe range
    decay_exponent = max(decay_exponent, -700)   # exp(-700) ~ 5e-305
    drift_exponent = max(drift_exponent, -700)

    time_component = math.exp(decay_exponent)
    drift_component = math.exp(drift_exponent)

    confidence = time_component * drift_component

    # Hard clamp
    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence


# ---- Aggregation ----

def aggregate_observations(
    observations: List[Observation],
    now: Optional[datetime] = None
) -> float:
    """
    Deterministic aggregation with trust × recency weighting.
    """

    if not observations:
        return 0.0

    now = now or datetime.utcnow()

    weighted_sum = 0.0
    total_weight = 0.0

    for obs in observations:
        if obs is None:
            continue

        # Sanitize trust
        trust = min(max(obs.trust, 0.0), 1.0)

        # Compute age safely
        age = (now - obs.timestamp).total_seconds()

        # Guard against future timestamps
        age = max(0.0, age)

        # Stable decay
        exponent = -DECAY_LAMBDA * age
        exponent = max(exponent, -700)

        recency_weight = math.exp(exponent)

        weight = trust * recency_weight

        # Skip useless weights
        if weight <= 0.0:
            continue

        weighted_sum += obs.value * weight
        total_weight += weight

    if total_weight <= EPSILON:
        return 0.0

    return weighted_sum / total_weight


# ---- Full Pipeline ----

def evaluate_account(
    claimed: float,
    observations: List[Observation],
    last_verified: datetime,
    materiality: float = DEFAULT_MATERIALITY,
    now: Optional[datetime] = None
) -> Optional[AssuranceResult]:
    """
    Full triple-state evaluation with deterministic time.
    """

    now = now or datetime.utcnow()

    observed = aggregate_observations(observations, now=now)

    # Stable drift (critical fix)
    denominator = max(abs(claimed), EPSILON)
    relative_drift = abs(claimed - observed) / denominator

    # Time delta
    age = (now - last_verified).total_seconds()
    age = max(0.0, age)

    confidence = compute_confidence(relative_drift, age)

    # Risk function (bounded + stable)
    risk = relative_drift * (1.0 - confidence) * max(materiality, 0.0)

    return AssuranceResult(
        claimed=claimed,
        observed=observed,
        relative_drift=relative_drift,
        confidence=confidence,
        risk=risk,
    )
