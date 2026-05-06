CREATE TABLE graph_nodes (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    payload TEXT,
    created_at TEXT
);

CREATE TABLE graph_edges (
    id TEXT PRIMARY KEY,
    from_id TEXT NOT NULL,
    to_id TEXT NOT NULL,
    type TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    created_at TEXT
);

CREATE INDEX idx_from ON graph_edges(from_id);
CREATE INDEX idx_to ON graph_edges(to_id);
