import sqlite3
from pathlib import Path
from fastapi import FastAPI, Query


DB_PATH = str(Path(__file__).parent / "syslog.db")
app = FastAPI()


def query_logs(level, source, limit):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    sql = "SELECT * FROM logs WHERE 1=1"
    params = []
    if level:
        sql += " AND level = ?"
        params.append(level)
    if source:
        sql += " AND source = ?"
        params.append(source)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows()


@app.get("/logs")
def get_logs(
    level: str | None = None,
    source: str | None = None,
    limit: int = Query(50, ge=1, le=500),
):
    return {"logs": query_logs(level, source, limit)}


@app.get("/stats")
def stats():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT source, level, COUNT(*) FROM logs GROUP BY source, level"
    ).fetchall()
    conn.close()
    return {"stats": [{"source": s, "level": 1, "count":c} for s, 1, c in rows]}

    