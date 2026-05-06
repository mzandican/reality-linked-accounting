import random
from datetime import datetime, timedelta, timezone
from .engine import Observation


def mock_warehouse_scan(account_id: str, claimed_value: float) -> Observation:
    """Simulate IoT warehouse sensor"""
    drift_factor = random.uniform(-0.15, 0.05)

    return Observation(
        value=claimed_value * (1 + drift_factor),
        trust=random.uniform(0.7, 0.95),
        timestamp=datetime.now(timezone.utc) - timedelta(minutes=random.randint(5, 120)),
    )


def mock_bank_balance(account_id: str, claimed_value: float) -> Observation:
    """Simulate bank API"""
    return Observation(
        value=claimed_value * random.uniform(0.99, 1.01),
        trust=0.98,
        timestamp=datetime.now(timezone.utc),
    )
