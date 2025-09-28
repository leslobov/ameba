#!/usr/bin/env python3

import sys
import requests
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_training_api():
    """Test the training API endpoints"""
    base_url = "http://127.0.0.1:8000"

    print("Testing Training API...")

    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("Root response:", response.json())
    except Exception as e:
        print(f"Failed to connect to API: {e}")
        return False

    # Test training status
    try:
        response = requests.get(f"{base_url}/api/training/status")
        print(f"Training status endpoint status: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            print("Training status:", status)
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Failed to get training status: {e}")

    # Test training endpoint with minimal parameters
    try:
        training_data = {
            "steps": 100,  # Small number for testing
            "batch_size": 10,
            "mode": True,
        }

        print(f"Starting training with data: {training_data}")
        response = requests.post(f"{base_url}/api/training/train", json=training_data)
        print(f"Training endpoint status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("Training result:", result)
        else:
            print("Error:", response.text)

    except Exception as e:
        print(f"Failed to start training: {e}")

    return True


if __name__ == "__main__":
    test_training_api()
