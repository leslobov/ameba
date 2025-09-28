#!/usr/bin/env python3
"""
Simple FastAPI server starter for the training API
"""

import uvicorn

if __name__ == "__main__":
    print("Starting Ameba Training API Server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
