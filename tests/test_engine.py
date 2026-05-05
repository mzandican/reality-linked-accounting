"""Test suite for the confidence engine mathematical functions."""
from datetime import datetime, timedelta
from src.engine import compute_confidence, aggregate_observations, Observation


def test_perfect_confidence():
    """Test that perfect match with no time decay yields confidence of 1.0."""
    assert compute_confidence(0.0, 0) == 1.0


def test_drift_penalizes():
    """Test that relative drift reduces confidence score."""
    c = compute_confidence(0.2, 0)
    assert 0.0 < c < 1.0


def test_time_decay():
    """Test that confidence decays over time even with zero drift."""
    c1 = compute_confidence(0.0, 0)
    c2 = compute_confidence(0.0, 86400)  # 1 day in seconds
    assert c2 < c1
    assert c2 >= 0.0


def test_aggregation_weights():
    """Test that observation aggregation weights by trust and recency."""
    now = datetime.now()
    obs = [
        Observation(100, 1.0, now),
        Observation(120, 0.5, now - timedelta(hours=2)),
        Observation(80, 0.8, now - timedelta(hours=1))
    ]
    agg = aggregate_observations(obs)
    assert 90 < agg < 105  # Should lean toward recent, high-trust values


def test_bounds_enforced():
    """Test that confidence is always bounded between 0 and 1."""
    assert 0.0 <= compute_confidence(1.5, 999999) <= 1.0
