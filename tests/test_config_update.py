#!/usr/bin/env python3
import requests
import json

# Test configuration update
config_data = {
    "play_desk": {
        "total_energy": 10000.0,
        "energy_per_food": 50.0,
        "rows": 32,
        "columns": 32,
    },
    "ameba": {
        "threhold_of_lostness_weight_coefficient": 0.2,
        "visible_rows": 5,
        "visible_columns": 5,
        "initial_energy": 100.0,
        "lost_energy_per_move": 1.0,
    },
    "neural_network": {"initial_hidden_layers": 1, "initial_neurons_on_layer": 32},
}

try:
    response = requests.put(
        "http://127.0.0.1:8000/api/config", json=config_data, timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
