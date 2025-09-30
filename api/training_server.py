#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import required modules
from core.neural_network.models.base import BaseNeuralNetwork
from core.config_classes.game_config import GameConfig

# FastAPI app
app = FastAPI(
    title="Ameba Neural Network Training API",
    description="API for training neural networks in the Ameba AI simulation",
    version="1.0.0",
)

# Configuration
CONFIG_FILE_PATH = project_root / "config.json"


# Models
class TrainingRequest(BaseModel):
    steps: int = 1000
    batch_size: int = 32
    mode: bool = True


class TrainingResponse(BaseModel):
    success: bool
    message: str
    steps_completed: Optional[int] = None


def load_game_config() -> GameConfig:
    """Load game configuration from config.json"""
    if not CONFIG_FILE_PATH.exists():
        raise HTTPException(status_code=404, detail="Configuration file not found")

    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config_data = json.load(file)
        return GameConfig.from_dict(config_data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load configuration: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Ameba Neural Network Training API",
        "version": "1.0.0",
        "endpoints": {
            "train": "/api/training/train",
            "status": "/api/training/status",
            "docs": "/docs",
        },
    }


@app.post("/api/training/train", response_model=TrainingResponse)
async def train_neural_network(request: TrainingRequest):
    """
    Train the neural network with specified parameters

    - **steps**: Number of training steps (default: 1000)
    - **batch_size**: Batch size for training (default: 32)
    - **mode**: Training mode (default: True)
    """
    try:
        print(
            f"Starting training with steps={request.steps}, batch_size={request.batch_size}"
        )

        # Load configuration
        game_config = load_game_config()

        # Create neural network instance
        neural_network = BaseNeuralNetwork(game_config.neural_network)

        # Train the neural network
        neural_network.train(
            steps=request.steps, batch_size=request.batch_size, mode=request.mode
        )

        # Save the trained model state
        net_state_path = (
            project_root / "core" / "neural_network" / "net_state" / "base.pth"
        )
        net_state_path.parent.mkdir(parents=True, exist_ok=True)

        import torch

        torch.save(neural_network._nn.state_dict(), net_state_path)

        print(f"Training completed and model saved to {net_state_path}")

        return TrainingResponse(
            success=True,
            message=f"Neural network training completed successfully. Model saved to {net_state_path}",
            steps_completed=request.steps,
        )

    except Exception as e:
        print(f"Training failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@app.get("/api/training/status")
async def get_training_status():
    """Get the current training status and model information"""
    try:
        net_state_path = (
            project_root / "core" / "neural_network" / "net_state" / "base.pth"
        )
        model_exists = net_state_path.exists()

        if model_exists:
            stat = net_state_path.stat()
            import datetime

            last_modified = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        else:
            last_modified = None

        return {
            "model_exists": model_exists,
            "model_path": str(net_state_path),
            "last_modified": last_modified,
            "config_exists": CONFIG_FILE_PATH.exists(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get training status: {str(e)}"
        )


if __name__ == "__main__":
    print("Starting Ameba Neural Network Training API...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
