from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uvicorn

# Import the config module
from config import router as config_router

# Initialize FastAPI app
app = FastAPI(
    title="Ameba Game API",
    description="API for Ameba AI simulation game configuration and management",
    version="1.0.0",
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(config_router)

# Path to config file (for health check)
CONFIG_FILE_PATH = Path(__file__).parent.parent / "config.json"


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Ameba Game API",
        "version": "1.0.0",
        "endpoints": {"config": "/api/config", "health": "/health", "docs": "/docs"},
        "modules": ["config"],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "config_file_exists": CONFIG_FILE_PATH.exists(),
        "modules_loaded": ["config"],
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
