def detect_anomaly(observed, claimed):
    if claimed == 0:
        return 1.0

    drift = abs(observed - claimed) / claimed
    return drift
