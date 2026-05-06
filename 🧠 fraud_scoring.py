def compute_risk(node_trust: float, drift: float, graph_pressure: float):
    """
    Combine signals into fraud score
    """

    risk = (1 - node_trust) * 0.4 + abs(drift) * 0.4 + graph_pressure * 0.2

    return min(max(risk, 0.0), 1.0)
