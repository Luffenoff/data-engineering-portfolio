from fastapi import FastAPI
from pydantic import BaseModel
import asyncio


app = FastAPI()


events: list[dict] = []


class TelemetryEvent(BaseModel):
    source: str
    message: str
    level: str = "info"
    
    
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/telemetry")
async def receive_telemetry(event: TelemetryEvent):
    await asyncio.sleep(0) # просто заглушка
    print(f"[{event.level.upper()}] {event.source}: {event.message}")
    return {"received": True, "source": event.source}