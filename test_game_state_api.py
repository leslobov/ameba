#!/usr/bin/env python3
"""
Test script for the new Game State API endpoint
"""

import requests
import json


def test_game_state_api():
    """Test the new /api/movement/state endpoint"""

    base_url = "http://127.0.0.1:8000"
    endpoint = f"{base_url}/api/movement/state"

    print("🔍 Testing Game State API Endpoint")
    print(f"📡 Endpoint: {endpoint}")
    print("=" * 50)

    try:
        # Test the game state endpoint
        response = requests.get(endpoint)

        if response.status_code == 200:
            data = response.json()

            print("✅ API Response Successful!")
            print(f"   Success: {data['success']}")
            print(f"   Message: {data['message']}")
            print(f"   Ameba Count: {data['ameba_count']}")
            print(f"   Food Count: {data['food_count']}")
            print(
                f"   Board Size: {data['board_size']['rows']}x{data['board_size']['columns']}"
            )

            # Show first ameba and food positions
            if data["game_state"]["amebas"]:
                ameba = data["game_state"]["amebas"][0]
                print(
                    f"   First Ameba: Position({ameba['position']['row']}, {ameba['position']['column']}) Energy: {ameba['energy']}"
                )

            if data["game_state"]["foods"]:
                food = data["game_state"]["foods"][0]
                print(
                    f"   First Food: Position({food['position']['row']}, {food['position']['column']}) Energy: {food['energy']}"
                )

            print("\n🎯 Backend Game State Retrieved Successfully!")
            print("   This represents the actual PlayDesk state from the Game class")

        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on port 8000")
        print("   Run: cd /home/les/projects/ai/ameba/api && python3 main.py")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_game_state_api()
