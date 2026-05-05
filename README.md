# Reality-Linked Accounting (RLA) v2.0

Append-only, triple-state accounting system. Tracks `Claimed ↔ Observed ↔ Confidence` with normalized drift, time decay, and cryptographic audit chains.

## 🔑 Core Fixes (Peer-Reviewed)
- ✅ Normalized relative drift: `d_r = |C-O| / max(|C|, ε)`
- ✅ Decoupled decay: `C = e^(-λt) × e^(-k·d_r)` → bounded [0,1]
- ✅ Weighted observation aggregation (trust × recency)
- ✅ Append-only assurance ledger (immutable history)
- ✅ Normalized risk: `R = d_r × (1-C) × M`

## 🚀 Quick Start
```bash
pip install -r requirements.txt
python scripts/init_db.py
uvicorn src.api:app --reload
```
API Docs: `http://localhost:8000/docs`

## 📊 Submit Assurance
```json
POST /assure
{
  "account_id": "INV-001",
  "claimed": 1000000,
  "observations": [
    {"value": 820000, "trust": 0.9, "timestamp": "2024-01-01T12:00:00Z"},
    {"value": 835000, "trust": 0.7, "timestamp": "2024-01-01T10:00:00Z"}
  ],
  "materiality": 1.0
}
```

## 🛡️ Audit Integrity
- Hash-chained records (`prev_hash`)
- Zero UPDATE/DELETE operations
- Full historical replay available via `/accounts/{id}/history`

## 📜 License
MIT
