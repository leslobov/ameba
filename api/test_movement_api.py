#!/usr/bin/env python3
"""
Test script for ameba movement API
"""

import requests
import json
import sys
from pathlib import Path

# API base URL
BASE_URL = "http://127.0.0.1:8000"


def test_movement_status():
    """Test movement status endpoint"""
    print("Testing movement status...")
    try:
        response = requests.get(f"{BASE_URL}/api/movement/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_simple_move():
    """Test simple ameba movement"""
    print("\nTesting simple ameba movement...")
    try:
        payload = {"iterations": 1}
        response = requests.post(f"{BASE_URL}/api/movement/move", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_multiple_moves():
    """Test multiple movement iterations"""
    print("\nTesting multiple movement iterations...")
    try:
        payload = {"iterations": 3}
        response = requests.post(f"{BASE_URL}/api/movement/move", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_simulation():
    """Test game simulation"""
    print("\nTesting game simulation...")
    try:
        payload = {"iterations": 5, "return_steps": False}
        response = requests.post(f"{BASE_URL}/api/movement/simulate", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_simulation_with_steps():
    """Test game simulation with step recording"""
    print("\nTesting game simulation with steps...")
    try:
        payload = {"iterations": 2, "return_steps": True}
        response = requests.post(f"{BASE_URL}/api/movement/simulate", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=== Ameba Movement API Tests ===\n")

    tests = [
        ("Movement Status", test_movement_status),
        ("Simple Move", test_simple_move),
        ("Multiple Moves", test_multiple_moves),
        ("Simulation", test_simulation),
        ("Simulation with Steps", test_simulation_with_steps),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        result = test_func()
        results.append((test_name, result))
        print(f"{'='*50}")

    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY:")
    print(f"{'='*50}")

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\nTotal: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
