from datetime import datetime, timedelta
from src.engine import compute_confidence, aggregate_observations, Observation

def test_perfect_confidence():
    assert compute_confidence(0.0, 0) == 1.0

def test_drift_penalizes():
    c = compute_confidence(0.2, 0)
    assert 0.0 < c < 1.0

def test_time_decay():
    c1 = compute_confidence(0.0, 0)
    c2 = compute_confidence(0.0, 86400)  # 1 day
    assert c2 < c1
    assert c2 >= 0.0

def test_aggregation_weights():
    now = datetime.now()
    obs = [
        Observation(100, 1.0, now),
        Observation(120, 0.5, now - timedelta(hours=2)),
        Observation(80, 0.8, now - timedelta(hours=1))
    ]
    agg = aggregate_observations(obs)
    assert 90 < agg < 105  # Should lean toward recent, high-trust

def test_bounds_enforced():
    assert 0.0 <= compute_confidence(1.5, 999999) <= 1.0
