#!/usr/bin/env python3
"""
Comprehensive test script for the Ameba Movement API.
Tests all endpoints with various scenarios.
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"


def test_endpoint(name, method, endpoint, data=None):
    """Test an API endpoint and print results"""
    print(f"\n=== Testing {name} ===")
    url = f"{BASE_URL}{endpoint}"

    try:
        response = None
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)

        if response:
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("✅ SUCCESS")
                result = response.json()
                print(
                    json.dumps(result, indent=2)[:500] + "..."
                    if len(json.dumps(result, indent=2)) > 500
                    else json.dumps(result, indent=2)
                )
            else:
                print("❌ FAILED")
                print(response.text)
        else:
            print("❌ UNSUPPORTED METHOD")
    except Exception as e:
        print(f"❌ ERROR: {e}")


def main():
    print("🧬 Ameba Movement API Test Suite")
    print("=" * 50)

    # Test basic endpoints
    test_endpoint("Root Endpoint", "GET", "/")
    test_endpoint("Health Check", "GET", "/health")
    test_endpoint("Movement Status", "GET", "/api/movement/status")

    # Test movement endpoint
    move_request = {
        "game_state": {
            "amebas": [
                {"type": "ameba", "energy": 100.0, "position": {"row": 5, "column": 5}}
            ],
            "foods": [
                {"type": "food", "energy": 50.0, "position": {"row": 4, "column": 5}}
            ],
            "board_size": {"rows": 12, "columns": 12},
        },
        "ameba_id": None,
        "iterations": 1,
    }
    test_endpoint("Single Movement", "POST", "/api/movement/move", move_request)

    # Test simulation endpoint
    simulation_request = {
        "game_state": {
            "amebas": [
                {"type": "ameba", "energy": 100.0, "position": {"row": 6, "column": 6}}
            ],
            "foods": [
                {"type": "food", "energy": 50.0, "position": {"row": 5, "column": 6}},
                {"type": "food", "energy": 50.0, "position": {"row": 7, "column": 6}},
            ],
            "board_size": {"rows": 12, "columns": 12},
        },
        "iterations": 5,
        "return_intermediate_states": False,
    }
    test_endpoint(
        "Multi-Step Simulation", "POST", "/api/movement/simulate", simulation_request
    )

    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")


if __name__ == "__main__":
    main()
