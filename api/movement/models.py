from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Position(BaseModel):
    """Position on the game board"""

    row: int = Field(..., ge=0, description="Row position (0-based)")
    column: int = Field(..., ge=0, description="Column position (0-based)")


class CellEntity(BaseModel):
    """Entity in a game cell"""

    type: str = Field(..., description="Type of entity: 'empty', 'food', 'ameba'")
    energy: Optional[float] = Field(None, description="Energy value if applicable")
    position: Position


class GameState(BaseModel):
    """Current state of the game board"""

    amebas: List[CellEntity] = Field(
        default_factory=list, description="List of amebas on the board"
    )
    foods: List[CellEntity] = Field(
        default_factory=list, description="List of food items on the board"
    )
    board_size: Dict[str, int] = Field(
        ..., description="Board dimensions (rows, columns)"
    )


class MoveRequest(BaseModel):
    """Request to move amebas"""

    game_state: Optional[GameState] = Field(
        None,
        description="Current game state (optional - will load from config if not provided)",
    )
    ameba_id: Optional[int] = Field(
        None, description="Specific ameba ID to move (if None, moves all)"
    )
    iterations: int = Field(
        1, ge=1, le=100, description="Number of movement iterations"
    )


class FoodGenerationInfo(BaseModel):
    """Information about food generation during movement"""

    total_foods_consumed: int = Field(0, description="Total number of foods consumed")
    total_foods_generated: int = Field(0, description="Total number of foods generated")
    net_food_change: int = Field(
        0, description="Net change in food count (generated - consumed)"
    )


class MovementResult(BaseModel):
    """Result of an ameba movement"""

    ameba_position: Position = Field(..., description="Ameba's position")
    old_position: Position = Field(..., description="Previous position")
    new_position: Position = Field(..., description="New position after movement")
    energy_change: float = Field(0.0, description="Energy gained/lost during movement")
    food_consumed: Optional[Position] = Field(
        None, description="Position of food consumed, if any"
    )


class MoveResponse(BaseModel):
    """Response from ameba movement API"""

    success: bool = Field(..., description="Whether the movement was successful")
    message: str = Field(..., description="Status message")
    movements: List[MovementResult] = Field(
        default_factory=list, description="List of movement results"
    )
    updated_game_state: Optional[GameState] = Field(
        None, description="Updated game state after movements"
    )
    iterations_completed: int = Field(0, description="Number of iterations completed")
    food_generation: Optional[FoodGenerationInfo] = Field(
        None, description="Information about food generation during movement"
    )


class SimulationRequest(BaseModel):
    """Request to run a full game simulation"""

    iterations: int = Field(10, ge=1, le=1000, description="Number of simulation steps")
    return_steps: bool = Field(
        False, description="Whether to return intermediate steps"
    )


class SimulationStep(BaseModel):
    """Single step in game simulation"""

    step_number: int = Field(..., description="Step number in simulation")
    movements: List[MovementResult] = Field(
        default_factory=list, description="Movements in this step"
    )
    game_state: GameState = Field(..., description="Game state after this step")
    total_energy: float = Field(..., description="Total energy in the system")


class SimulationResponse(BaseModel):
    """Response from game simulation"""

    success: bool = Field(..., description="Whether the simulation was successful")
    message: str = Field(..., description="Status message")
    total_iterations: int = Field(..., description="Total iterations completed")
    final_game_state: GameState = Field(..., description="Final state of the game")
    steps: Optional[List[SimulationStep]] = Field(
        None, description="Intermediate steps if requested"
    )
    statistics: Dict[str, Any] = Field(
        default_factory=dict, description="Simulation statistics"
    )
