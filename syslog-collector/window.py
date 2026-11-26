import sqlite3
from pathlib import Path


conn = sqlite3.connect(Path(__file__).parent / "syslog.db")


# Нарастающий итог ошибок по источнику
q1 = """
SELECT id, source, level,
       COUNT(*) OVER (PARTITION BY source ORDER BY id) AS running_cnt
FROM logs
WHERE level = 'error'
LIMIT 10
"""


