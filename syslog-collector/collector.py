import asyncio
import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = str(Path(__file__).parent / "syslog.db")
BATCH_SIZE = 100
FLUSH_INTERVAL = 1.0  # секунд


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at TEXT,
            source TEXT,
            level TEXT,
            message TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_source ON logs(source)")
    conn.commit()
    conn.close()


def save_batch(rows: list[tuple]):
    conn = sqlite3.connect(DB_PATH)
    conn.executemany(
        "INSERT INTO logs (received_at, source, level, message) VALUES (?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()


class SyslogProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def datagram_received(self, data, addr):
        try:
            event = json.loads(data.decode("utf-8"))
            row = (
                datetime.now(timezone.utc).isoformat(),
                event.get("source", "unknown"),
                event.get("level", "info"),
                event.get("message", ""),
            )
            self.queue.put_nowait(row)
        except Exception as e:
            print(f"Parse error from {addr}: {e}")


async def writer(queue: asyncio.Queue):
    batch = []
    while True:
        try:
            row = await asyncio.wait_for(queue.get(), timeout=FLUSH_INTERVAL)
            batch.append(row)
        except asyncio.TimeoutError:
            pass
        if batch and (len(batch) >= BATCH_SIZE or queue.empty()):
            await asyncio.to_thread(save_batch, batch)
            print(f"Записано пачкой: {len(batch)}")
            batch = []


async def main():
    init_db()
    queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: SyslogProtocol(queue), local_addr=("127.0.0.1", 5140)
    )
    print(f"DB: {DB_PATH}")
    print("Syslog collector запущен на UDP 127.0.0.1:5140")
    try:
        await writer(queue)
    finally:
        transport.close()


asyncio.run(main())