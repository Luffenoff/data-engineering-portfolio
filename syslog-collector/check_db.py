import sqlite3
from pathlib import Path


db = Path(__file__).parent / "syslog.db"
conn = sqlite3.connect(db)

total = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
stress = conn.execute("SELECT COUNT(*) FROM logs WHERE source = 'stress'").fetchone()[0]
print(f"Всего записей: {total}")
print(f"Из stress-теста: {stress}")
conn.close()