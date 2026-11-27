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


# Lag предыдущая запись того же источника
q2 = """
SELECT id, source, received_at,
        LAG(received_at) OVER (PARTITION BY source ORDER BY id) AS prev_received_at
FROM logs
LIMIT 10
"""


# Последняя запись каждого источника
q3 = """
SELECT source, received_at, message FROM(
    SELECT *, ROW_NUMBER() OVER (PARTITION BY source ORDER BY id DESC) AS rn
    FROM logs
) WHERE rn = 1
"""


for name, q in [("running", q1), ("lag", q2), ("last per source", q3)]:
    print(f"--- {name}")
    for row in conn.execute(q):
        print(row)
