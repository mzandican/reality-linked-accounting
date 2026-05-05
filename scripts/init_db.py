from src.repository import init_db
print("Initializing append-only assurance ledger...")
init_db()
print("✅ rla_assurance.db ready. All writes are immutable.")
