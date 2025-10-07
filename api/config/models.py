from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Literal, Optional


class PlayDeskConfig(BaseModel):
    """Play desk configuration model"""

    total_energy: float = Field(
        default=10000.0, ge=1000.0, le=100000.0, description="Total energy in the world"
    )
    energy_per_food: float = Field(
        default=50.0, ge=10.0, le=200.0, description="Energy value per food item"
    )
    rows: int = Field(
        default=32, ge=10, le=100, description="Number of rows in the world grid"
    )
    columns: int = Field(
        default=32, ge=10, le=100, description="Number of columns in the world grid"
    )


class AmebaConfig(BaseModel):
    """Ameba configuration model"""

    threhold_of_lostness_weight_coefficient: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="Threshold coefficient for lostness weight",
    )
    visible_rows: int = Field(
        default=5, ge=3, le=15, description="Number of visible rows for ameba"
    )
    visible_columns: int = Field(
        default=5, ge=3, le=15, description="Number of visible columns for ameba"
    )
    initial_energy: float = Field(
        default=100.0, ge=50.0, le=500.0, description="Initial energy for new amebas"
    )
    lost_energy_per_move: float = Field(
        default=1.0, ge=0.1, le=10.0, description="Energy lost per movement"
    )


class NeuralNetworkConfig(BaseModel):
    """Neural network configuration model"""

    initial_hidden_layers: int = Field(
        default=1, ge=0, le=10, description="Number of initial hidden layers"
    )
    initial_neurons_on_layer: int = Field(
        default=32, ge=4, le=256, description="Number of neurons per layer"
    )


class GameConfig(BaseModel):
    """Complete game configuration model"""

    play_desk: PlayDeskConfig
    ameba: AmebaConfig
    neural_network: NeuralNetworkConfig


class ConfigUpdateRequest(BaseModel):
    """Request model for updating configuration"""

    config: GameConfig


class ConfigSectionRequest(BaseModel):
    """Request model for updating a specific configuration section"""

    data: Dict[str, Any]


class ApiResponse(BaseModel):
    """Standard API response model"""

    success: bool
    message: str
    data: Dict[str, Any] | None = None


class ConfigSectionResponse(ApiResponse):
    """Response model for configuration section operations"""

    section: str | None = None


# Type for valid configuration sections
ConfigSection = Literal["play_desk", "ameba", "neural_network"]
