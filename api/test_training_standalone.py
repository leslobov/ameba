#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_training():
    """Test the training functionality directly"""

    print("=" * 60)
    print("TESTING NEURAL NETWORK TRAINING")
    print("=" * 60)

    # Test imports
    try:
        from src.neural_network.models.base import BaseNeuralNetwork
        from src.config_classes.game_config import GameConfig

        print("✓ Neural network imports successful")
    except Exception as e:
        print(f"✗ Neural network import failed: {e}")
        return False

    # Test config loading
    try:
        config_path = project_root / "config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                config_data = json.load(f)
            game_config = GameConfig.from_dict(config_data)
            print("✓ Configuration loading successful")
            print(f"  - Neural network config: {game_config.neural_network}")
        else:
            print("✗ Configuration file not found")
            return False
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

    # Test neural network creation
    try:
        neural_network = BaseNeuralNetwork(game_config.neural_network)
        print("✓ Neural network creation successful")
    except Exception as e:
        print(f"✗ Neural network creation failed: {e}")
        return False

    # Test training (small scale for testing)
    try:
        print("Starting training test...")
        print("  Parameters: steps=50, batch_size=5")

        neural_network.train(steps=50, batch_size=5, mode=True)

        print("✓ Training completed successfully!")

        # Test saving model state
        net_state_path = (
            project_root / "src" / "neural_network" / "net_state" / "base.pth"
        )
        net_state_path.parent.mkdir(parents=True, exist_ok=True)

        import torch

        torch.save(neural_network._nn.state_dict(), net_state_path)
        print(f"✓ Model saved to: {net_state_path}")

    except Exception as e:
        print(f"✗ Training failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    print("=" * 60)
    print("ALL TESTS PASSED! 🎉")
    print("The training API is ready to use.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_training()
    sys.exit(0 if success else 1)
