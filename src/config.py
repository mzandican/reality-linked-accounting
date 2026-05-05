import os

# Confidence & Risk Parameters
EPSILON = 1e-6
DECAY_LAMBDA = 0.00005      # Time decay per second
DRIFT_PENALTY_K = 5.0       # Drift sensitivity
DEFAULT_MATERIALITY = 1.0   # Scale control

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///rla_assurance.db")
