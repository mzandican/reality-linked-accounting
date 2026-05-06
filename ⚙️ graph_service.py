from .fraud_scoring import compute_risk
from .anomaly_detection import detect_anomaly

def evaluate_fraud(claimed, observed, trust, graph_pressure=0.0):

    drift = detect_anomaly(observed, claimed)

    risk = compute_risk(
        node_trust=trust,
        drift=drift,
        graph_pressure=graph_pressure
    )

    return {
        "drift": drift,
        "risk": risk,
        "status": "HIGH" if risk > 0.7 else "LOW"
    }
