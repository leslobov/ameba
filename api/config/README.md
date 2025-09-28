# Config Module

This module handles all configuration-related operations for the Ameba Game API.

## Structure

```
config/
├── __init__.py          # Module initialization and exports
├── models.py            # Pydantic models for configuration data
├── service.py           # Business logic for configuration operations  
├── router.py            # FastAPI routes for configuration endpoints
└── README.md            # This file
```

## Models

### GameConfig
Complete game configuration containing all sections:
- `play_desk`: World/environment settings
- `ameba`: Ameba behavior settings  
- `neural_network`: AI/neural network settings

### Individual Section Models
- `PlayDeskConfig`: World grid, energy settings
- `AmebaConfig`: Ameba properties, movement costs
- `NeuralNetworkConfig`: Network architecture settings

## Service Layer

The `ConfigService` class handles:
- Loading/saving configuration from/to JSON file
- Data validation using Pydantic models
- Configuration section management
- Default value reset

## API Endpoints

All endpoints are prefixed with `/api/config`:

### Core Operations
- `GET /` - Get complete configuration
- `PUT /` - Update complete configuration  
- `POST /reset` - Reset to default values

### Section Operations
- `GET /{section}` - Get specific section (play_desk, ameba, neural_network)
- `PUT /{section}` - Update specific section

### Utility Operations
- `GET /info/status` - Get configuration file information
- `GET /validate` - Validate current configuration

## Usage Example

```python
from config import ConfigService, GameConfig

# Initialize service
service = ConfigService(Path("config.json"))

# Load configuration
config = service.get_config()

# Update configuration
new_config = GameConfig(...)
service.update_config(new_config)

# Update specific section
service.update_config_section("play_desk", {"rows": 40, "columns": 40})
```

## Data Validation

All configuration data is validated using Pydantic models with:
- Type checking
- Range validation (min/max values)
- Required field validation
- Custom business logic validation

## Error Handling

The module provides comprehensive error handling:
- File not found errors
- JSON parsing errors  
- Validation errors
- Generic exceptions with detailed messages