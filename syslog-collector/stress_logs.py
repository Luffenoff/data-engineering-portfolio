import socket
import json


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(2000):
    log = {"source": "stress", "level": "info", "message": f"msg{i}"}
    sock.sendto(json.dumps(log).encode(), ("127.0.0.1", 5140))
sock.close()
print("Stress test completed: 2000 log messages sent.")