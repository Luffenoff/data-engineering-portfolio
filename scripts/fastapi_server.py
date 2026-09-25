from fastapi import FastAPI
from pydantic import BaseModel
import asyncio


app = FastAPI()


class TelemetryEvent(BaseModel):
    source: str
    message: str
    level: str = "info"
    
    
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/")