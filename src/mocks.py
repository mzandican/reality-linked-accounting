import random
from datetime import datetime, timedelta
from .engine import Observation


def mock_warehouse_scan(account_id: str, claimed_value: float) -> Observation:
    """Simulate IoT warehouse reading"""
    drift_factor = random.uniform(-0.15, 0.05)
    observed = claimed_value * (1 + drift_factor)

    return Observation(
        value=observed,
        trust=random.uniform(0.7, 0.95),
        timestamp=datetime.utcnow() - timedelta(minutes=random.randint(5, 120))
    )


def mock_bank_balance(account_id: str, claimed_value: float) -> Observation:
    """Simulate bank API reading"""
    return Observation(
        value=claimed_value * random.uniform(0.99, 1.01),
        trust=0.98,
        timestamp=datetime.utcnow()
  )
