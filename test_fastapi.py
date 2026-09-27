import httpx

messages = ["connection established", "packet received", "timeout error"]

for msg in messages:
    r = httpx.post("http://127.0.0.1:8001/telemetry", json={
        "source": "tcp_collector",
        "message": msg,
        "level": "info"
    })
    print(r.json())

r = httpx.get("http://127.0.0.1:8001/events")
print(r.json())