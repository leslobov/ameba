import os
import sys
import json
from fastapi import APIRouter, HTTPException
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from training.models import TrainingRequest, TrainingResponse
from src.neural_network.models.base import BaseNeuralNetwork
from src.config_classes.game_config import GameConfig

router = APIRouter(prefix="/api/training", tags=["training"])

# Configuration loading
CONFIG_FILE_PATH = project_root / "config.json"


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


@router.post("/train", response_model=TrainingResponse)
async def train_neural_network(request: TrainingRequest):
    """
    Train the neural network with specified parameters

    - **steps**: Number of training steps (default: 10000)
    - **batch_size**: Batch size for training (default: 64)
    - **mode**: Training mode (default: True)
    """
    try:
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
            project_root / "src" / "neural_network" / "net_state" / "base.pth"
        )
        net_state_path.parent.mkdir(parents=True, exist_ok=True)

        import torch

        torch.save(neural_network._nn.state_dict(), net_state_path)

        return TrainingResponse(
            success=True,
            message=f"Neural network training completed successfully. Model saved to {net_state_path}",
            steps_completed=request.steps,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/status")
async def get_training_status():
    """Get the current training status and model information"""
    try:
        net_state_path = (
            project_root / "src" / "neural_network" / "net_state" / "base.pth"
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
