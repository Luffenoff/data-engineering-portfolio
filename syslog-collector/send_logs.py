import socket
import json
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


logs = [
    {"source": "nginx", "level": "info", "message": "GET /index 200"},
    {"source": "nginx", "level": "error", "message": "upstream timed out"},
    {"source": "postgres", "level": "warning", "message": "slow query 2300ms"},
    {"source": "api_server", "level": "info", "message": "POST /telemetry 200"},
    {"source": "api_server", "level": "error", "message": "POST /telemetry 500"},
]


for log in logs:
    sock.sendto(json.dumps(log).encode('utf-8'), ('127.0.0.1', 5140))
    