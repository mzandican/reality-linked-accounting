import sqlite3
import json

class GraphDB:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_node(self, node_id, node_type, payload):
        self.conn.execute(
            "INSERT INTO graph_nodes VALUES (?, ?, ?, datetime('now'))",
            (node_id, node_type, json.dumps(payload))
        )

    def add_edge(self, from_id, to_id, edge_type, weight):
        self.conn.execute(
            "INSERT INTO graph_edges VALUES (?, ?, ?, ?, ?, datetime('now'))",
            (f"{from_id}-{to_id}", from_id, to_id, edge_type, weight)
        )
