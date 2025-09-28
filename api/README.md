# Ameba Game API Server

A FastAPI-based REST API server for managing Ameba AI game configuration.

## 🚀 Quick Start

### Installation

1. **Activate virtual environment:**
   ```bash
   cd /home/les/projects/ai/ameba
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   cd api
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python main.py
   # or
   ./start.sh
   ```

4. **Test the API:**
   ```bash
   ./test_api.sh
   ```

## 📡 API Endpoints

### Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `GET` | `/api/config` | Get complete configuration |
| `PUT` | `/api/config` | Update complete configuration |
| `GET` | `/api/config/{section}` | Get specific section |
| `PUT` | `/api/config/{section}` | Update specific section |
| `POST` | `/api/config/reset` | Reset to defaults |

### Configuration Sections

- **`play_desk`** - World/environment settings
- **`ameba`** - Organism/entity settings  
- **`neural_network`** - AI/ML settings

## 📋 API Examples

### Get Configuration
```bash
curl "http://127.0.0.1:8000/api/config"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "play_desk": {
      "total_energy": 10000.0,
      "energy_per_food": 50.0,
      "rows": 32,
      "columns": 32
    },
    "ameba": {
      "threhold_of_lostness_weight_coefficient": 0.2,
      "visible_rows": 5,
      "visible_columns": 5,
      "initial_energy": 100.0,
      "lost_energy_per_move": 1.0
    },
    "neural_network": {
      "initial_hidden_layers": 1,
      "initial_neurons_on_layer": 32
    }
  },
  "message": "Configuration loaded successfully"
}
```

### Update Configuration
```bash
curl -X PUT "http://127.0.0.1:8000/api/config" \
  -H "Content-Type: application/json" \
  -d '{
    "play_desk": {
      "total_energy": 15000.0,
      "energy_per_food": 75.0,
      "rows": 40,
      "columns": 40
    },
    "ameba": {
      "threhold_of_lostness_weight_coefficient": 0.3,
      "visible_rows": 7,
      "visible_columns": 7,
      "initial_energy": 150.0,
      "lost_energy_per_move": 1.5
    },
    "neural_network": {
      "initial_hidden_layers": 2,
      "initial_neurons_on_layer": 64
    }
  }'
```

### Get Specific Section
```bash
curl "http://127.0.0.1:8000/api/config/play_desk"
```

### Reset to Defaults
```bash
curl -X POST "http://127.0.0.1:8000/api/config/reset"
```

## 🔧 Configuration Schema

### Play Desk Settings
```json
{
  "total_energy": 10000.0,      // Total energy in the world
  "energy_per_food": 50.0,      // Energy provided per food item
  "rows": 32,                   // World height in grid cells
  "columns": 32                 // World width in grid cells
}
```

### Ameba Settings
```json
{
  "threhold_of_lostness_weight_coefficient": 0.2,  // Weight coefficient for loss
  "visible_rows": 5,                               // Visible area height
  "visible_columns": 5,                            // Visible area width
  "initial_energy": 100.0,                         // Starting energy per ameba
  "lost_energy_per_move": 1.0                      // Energy cost per movement
}
```

### Neural Network Settings
```json
{
  "initial_hidden_layers": 1,      // Number of hidden layers
  "initial_neurons_on_layer": 32   // Neurons per layer
}
```

## 🌐 CORS Configuration

The API is configured to accept requests from:
- `http://localhost:4200` (Angular dev server)
- `http://127.0.0.1:4200`

## 🔍 Interactive Documentation

Once the server is running, visit:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## 📁 Project Structure

```
api/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── setup.sh            # Setup script
├── start.sh            # Start script
├── test_api.sh         # Test script
└── README.md           # This file
```

## 🛠 Development

### Running in Development Mode
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Testing
```bash
# Run the test script
./test_api.sh

# Manual testing with curl
curl "http://127.0.0.1:8000/health"
```

## 🔄 Integration with Frontend

The Angular frontend can consume this API using the `BackendApiService`:

```typescript
// Inject the service
private backendApi = inject(BackendApiService);

// Get configuration
this.backendApi.getGameConfig().subscribe(config => {
  console.log('Backend config:', config);
});

// Update configuration
this.backendApi.updateGameConfig(newConfig).subscribe(response => {
  console.log('Config updated:', response);
});
```

## 🚨 Error Handling

The API returns consistent error responses:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (validation error)
- `404` - Not Found (config section not found)
- `500` - Internal Server Error