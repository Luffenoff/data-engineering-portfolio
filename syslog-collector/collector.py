import asyncio
import sqlite3
import json
from datetime import datetime


DB_PATH = "syslog.db"


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
    conn.commit()
    conn.close()
    
    
def save_log(source: str, level: str, message: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO logs (received_at, source, level, message) VALUES (?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), source, level, message)
    )
    conn.commit()
    conn.close()
    
    
    
class SyslogProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        try:
            event = json.loads(data.decode('utf-8'))
            source = event.get('source', 'unknown')
            level = event.get('level', 'info')
            message = event.get('message', '')
            save_log(source, level, message)
            print(f"[{level.upper()}] {source}: {message}")
        except Exception as e:
            print(f"Parse error from {addr}: {e}")
            
            
async def main():
    init_db()
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        SyslogProtocol,
        local_addr=(127.0.0.1), 5140
    )
    print("Syslog collector запущен на UDP 127.0.0.1:5140")
    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()
        
        
asyncio.run(main())