"""Stress-tested suite for Reality-Linked Accounting engine."""
import sys
from pathlib import Path
from datetime import datetime, timedelta

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.engine import compute_confidence, aggregate_observations, Observation


FIXED_NOW = datetime(2024, 1, 1, 12, 0, 0)


def test_perfect_confidence():
    assert compute_confidence(0.0, 0) == 1.0


def test_drift_penalizes():
    c = compute_confidence(0.3, 0)
    assert 0.0 < c < 1.0


def test_time_decay():
    c1 = compute_confidence(0.0, 0)
    c2 = compute_confidence(0.0, 86400)
    assert c2 < c1


def test_bounds_extreme():
    c = compute_confidence(999, 1e9)
    assert 0.0 <= c <= 1.0


def test_future_timestamp_protection():
    obs = [
        Observation(100, 1.0, FIXED_NOW + timedelta(hours=1)),  # future
    ]
    agg = aggregate_observations(obs, now=FIXED_NOW)
    assert agg == 100


def test_zero_weight_collapse():
    obs = [
        Observation(100, 0.0, FIXED_NOW),
        Observation(200, 0.0, FIXED_NOW),
    ]
    assert aggregate_observations(obs, now=FIXED_NOW) == 0.0


def test_adversarial_outlier():
    obs = [
        Observation(100, 1.0, FIXED_NOW),
        Observation(1000000, 0.01, FIXED_NOW),
    ]
    agg = aggregate_observations(obs, now=FIXED_NOW)

    # Outlier must not dominate
    assert agg < 1000


def test_recency_bias():
    obs = [
        Observation(100, 1.0, FIXED_NOW),
        Observation(200, 1.0, FIXED_NOW - timedelta(days=10)),
    ]
    agg = aggregate_observations(obs, now=FIXED_NOW)
    assert agg < 150


def test_stability_small_values():
    c = compute_confidence(1e-12, 1e-12)
    assert 0.99 < c <= 1.0
