import random
from datetime import datetime, timedelta
from .engine import Observation

def mock_warehouse_scan(account_id: str, claimed_value: float) -> Observation:
    """Simulate IoT sensor reading with realistic drift"""
    drift_factor = random.uniform(-0.15, 0.05)  # -15% to +5% typical shrinkage
    observed = claimed_value * (1 + drift_factor)
    trust = random.uniform(0.7, 0.95)  # Sensor reliability
    
    return Observation(
        value=observed,
        trust=trust,
        timestamp=datetime.now() - timedelta(minutes=random.randint(5, 120))
    )

def mock_bank_balance(account_id: str, claimed_value: float) -> Observation:
    """Simulate bank API response"""
    return Observation(
        value=claimed_value * random.uniform(0.99, 1.01),  # ±1% typical
        trust=0.98,
        timestamp=datetime.now()
  )
