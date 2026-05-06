import os

EPSILON = 1e-6
DECAY_LAMBDA = 0.00005
DRIFT_PENALTY_K = 5.0
DEFAULT_MATERIALITY = 1.0

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///rla_assurance.db")
