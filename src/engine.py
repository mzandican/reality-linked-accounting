import math
from datetime import datetime
from dataclasses import dataclass
from typing import List
from .config import EPSILON, DECAY_LAMBDA, DRIFT_PENALTY_K, DEFAULT_MATERIALITY

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

def aggregate_observations(observations: List[Observation]) -> float | None:
    """Weighted aggregation: trust × recency decay."""
    if not observations:
        return None

    weighted_sum = 0.0
    total_weight = 0.0
    now = datetime.now()

    for obs in observations:
        age_seconds = (now - obs.timestamp).total_seconds()
        recency = math.exp(-0.0001 * age_seconds)  # Fast recency decay
        weight = obs.trust * recency
        weighted_sum += weight * obs.value
        total_weight += weight

    return weighted_sum / total_weight if total_weight > 0 else None

def compute_confidence(relative_drift: float, time_delta_seconds: float) -> float:
    """C = e^(-λt) × e^(-k × d_r) → bounded [0, 1]"""
    time_factor = math.exp(-DECAY_LAMBDA * time_delta_seconds)
    drift_factor = math.exp(-DRIFT_PENALTY_K * relative_drift)
    return max(0.0, min(1.0, time_factor * drift_factor))

def evaluate_account(claimed: float, observations: List[Observation], last_verified: datetime, materiality: float = DEFAULT_MATERIALITY) -> AssuranceResult | None:
    observed = aggregate_observations(observations)
    if observed is None:
        return None

    relative_drift = abs(claimed - observed) / max(abs(claimed), EPSILON)
    time_delta = (datetime.now() - last_verified).total_seconds()
    confidence = compute_confidence(relative_drift, time_delta)
    risk = relative_drift * (1.0 - confidence) * materiality

    return AssuranceResult(
        claimed=claimed,
        observed=observed,
        relative_drift=relative_drift,
        confidence=confidence,
        risk=risk
    )
