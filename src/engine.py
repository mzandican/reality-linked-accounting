"""Reality-Linked Accounting: Confidence & Aggregation Engine."""
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

def compute_confidence(drift: float, age_seconds: float,
                       lambda_decay: float = DECAY_LAMBDA,
                       k_drift: float = DRIFT_PENALTY_K) -> float:
    """
    Compute confidence based on normalized drift and time decay.
    C = e^(-λt) * e^(-k·d_r)  → strictly bounded [0, 1]
    """
    drift = max(0.0, drift)
    age_seconds = max(0.0, age_seconds)

    time_component = math.exp(-lambda_decay * age_seconds)
    drift_component = math.exp(-k_drift * drift)

    confidence = time_component * drift_component
    return max(0.0, min(1.0, confidence))

def aggregate_observations(observations: List[Observation]) -> float:
    """Weighted aggregation: trust × recency decay."""
    if not observations:
        return 0.0

    now = datetime.now()
    weighted_sum = 0.0
    total_weight = 0.0

    for obs in observations:
        age = (now - obs.timestamp).total_seconds()
        recency_weight = math.exp(-1e-5 * age)  # Consistent decay lambda
        weight = obs.trust * recency_weight

        weighted_sum += obs.value * weight
        total_weight += weight

    return weighted_sum / total_weight if total_weight > 0 else 0.0

def evaluate_account(claimed: float, observations: List[Observation], 
                     last_verified: datetime, materiality: float = DEFAULT_MATERIALITY) -> AssuranceResult | None:
    """Full triple-state evaluation pipeline."""
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
