"""
Training handler for API requests - interfaces with core neural network functionality
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from core.neural_network.models.base import BaseNeuralNetwork
from core.config_classes.game_config import GameConfig


@dataclass
class TrainingResult:
    """Result of training operation"""

    success: bool
    message: str
    steps_completed: int
    model_path: Optional[str] = None
    error_details: Optional[str] = None


@dataclass
class TrainingStatus:
    """Status of training model and configuration"""

    model_exists: bool
    model_path: str
    last_modified: Optional[str] = None
    config_exists: bool = True


class TrainingHandler:
    """Handler for neural network training operations"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_file_path = project_root / "config.json"
        self.model_save_path = (
            project_root / "core" / "neural_network" / "net_state" / "base.pth"
        )

    def load_game_config(self) -> GameConfig:
        """Load game configuration from config.json"""
        if not self.config_file_path.exists():
            raise FileNotFoundError("Configuration file not found")

        try:
            with open(self.config_file_path, "r") as file:
                config_data = json.load(file)
            return GameConfig.from_dict(config_data)
        except Exception as e:
            raise Exception(f"Failed to load configuration: {str(e)}")

    def train_neural_network(
        self, steps: int = 1000, batch_size: int = 32, mode: bool = True
    ) -> TrainingResult:
        """
        Train the neural network with specified parameters

        Args:
            steps: Number of training steps
            batch_size: Batch size for training
            mode: Training mode

        Returns:
            TrainingResult with operation details
        """
        try:
            # Load configuration
            game_config = self.load_game_config()

            # Create neural network instance
            neural_network = BaseNeuralNetwork(game_config.neural_network)

            # Train the neural network
            neural_network.train(steps=steps, batch_size=batch_size, mode=mode)

            # Save the trained model state
            self.model_save_path.parent.mkdir(parents=True, exist_ok=True)

            import torch

            torch.save(neural_network._nn.state_dict(), self.model_save_path)

            return TrainingResult(
                success=True,
                message=f"Neural network training completed successfully. Model saved to {self.model_save_path}",
                steps_completed=steps,
                model_path=str(self.model_save_path),
            )

        except Exception as e:
            return TrainingResult(
                success=False,
                message="Training failed",
                steps_completed=0,
                error_details=str(e),
            )

    def get_training_status(self) -> TrainingStatus:
        """Get the current training status and model information"""
        try:
            model_exists = self.model_save_path.exists()

            last_modified = None
            if model_exists:
                stat = self.model_save_path.stat()
                last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

            return TrainingStatus(
                model_exists=model_exists,
                model_path=str(self.model_save_path),
                last_modified=last_modified,
                config_exists=self.config_file_path.exists(),
            )

        except Exception as e:
            raise Exception(f"Failed to get training status: {str(e)}")
