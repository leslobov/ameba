#!/usr/bin/env python3
"""Simple test server to check API functionality."""

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Test server is running"}


@app.get("/api/movement/status")
async def movement_status():
    return {
        "status": "ok",
        "service": "movement",
        "message": "Movement service is operational",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False, log_level="info")
