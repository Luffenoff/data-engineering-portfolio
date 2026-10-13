from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import asyncio
import json

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    key_serializer=lambda k: k.encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

events: list[dict] = []

class TelemetryEvent(BaseModel):
    source: str
    message: str
    level: str = "info"

@app.get("/health")
async def health():
    return {"status": "ok", "events_count": len(events)}

@app.post("/telemetry")
async def receive_telemetry(event: TelemetryEvent):
    entry = event.model_dump()
    events.append(entry)
    
    # отправляем в Kafka
    producer.send(
        'telemetry',
        key=event.source,
        value=entry
    )
    
    print(f"[{event.level.upper()}] {event.source}: {event.message} → Kafka")
    return {"received": True, "total": len(events)}

@app.get("/events")
async def get_events():
    return {"events": events}