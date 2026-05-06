"""Test suite for Reality-Linked Accounting confidence engine."""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Fix Python path for GitHub Actions CI
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.engine import compute_confidence, aggregate_observations, Observation


def test_perfect_confidence():
    """Zero drift + zero time ⇒ exactly 1.0."""
    assert compute_confidence(0.0, 0) == 1.0


def test_drift_penalizes():
    """Drift must reduce confidence below 1.0."""
    c = compute_confidence(0.2, 0)
    assert 0.0 < c < 1.0


def test_time_decay():
    """Confidence must decay over time even with zero drift."""
    c1 = compute_confidence(0.0, 0)
    c2 = compute_confidence(0.0, 86400)  # 1 day
    assert c2 < c1
    assert c2 >= 0.0


def test_aggregation_weights():
    """Recent + high-trust observations dominate the aggregate."""
    now = datetime.now()
    obs = [
        Observation(100, 1.0, now),
        Observation(120, 0.5, now - timedelta(hours=2)),
        Observation(80, 0.8, now - timedelta(hours=1))
    ]
    agg = aggregate_observations(obs)
    # Bias toward 100, not 120
    assert abs(agg - 100) < abs(agg - 120)
    assert 85 < agg < 105  # Safety bounds


def test_bounds_enforced():
    """Confidence must never escape [0, 1] under extreme inputs."""
    assert 0.0 <= compute_confidence(1.5, 999999) <= 1.0
    assert 0.0 <= compute_confidence(0.0, 0) <= 1.0
