import json
import uuid
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def add_node(db, node_type: str, payload: dict):
    node_id = str(uuid.uuid4())

    db.execute(
        "INSERT INTO graph_nodes VALUES (?, ?, ?, ?)",
        (node_id, node_type, json.dumps(payload), now())
    )

    return node_id


def add_edge(db, from_id: str, to_id: str, edge_type: str, weight: float = 1.0):
    edge_id = str(uuid.uuid4())

    db.execute(
        "INSERT INTO graph_edges VALUES (?, ?, ?, ?, ?, ?)",
        (edge_id, from_id, to_id, edge_type, weight, now())
    )

    return edge_id
