import sys
from fastapi import APIRouter, HTTPException
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from movement.models import (
    MoveRequest,
    MoveResponse,
    SimulationRequest,
    SimulationResponse,
    MovementResult,
    GameState,
    Position,
    CellEntity,
    FoodGenerationInfo,
)
from core.out.movement_handler import MovementHandler

router = APIRouter(prefix="/api/movement", tags=["movement"])

# Initialize movement handler
movement_handler = MovementHandler(project_root)


@router.post("/move", response_model=MoveResponse)
async def move_amebas(request: MoveRequest):
    """
    Move amebas on the game board

    - **game_state**: Current game state (optional, uses internal state if not provided)
    - **ameba_id**: Specific ameba ID to move (optional, moves all if not provided)
    - **iterations**: Number of movement iterations (1-100)
    """
    try:
        # Convert Pydantic models to dictionaries for handler
        game_state_dict = None
        if request.game_state:
            game_state_dict = {
                "amebas": [
                    {
                        "type": ameba.type,
                        "energy": ameba.energy,
                        "position": {
                            "row": ameba.position.row,
                            "column": ameba.position.column,
                        },
                    }
                    for ameba in request.game_state.amebas
                ],
                "foods": [
                    {
                        "type": food.type,
                        "energy": food.energy,
                        "position": {
                            "row": food.position.row,
                            "column": food.position.column,
                        },
                    }
                    for food in request.game_state.foods
                ],
                "board_size": request.game_state.board_size,
            }

        # Use the movement handler
        result = movement_handler.move_amebas(
            game_state=game_state_dict,
            ameba_id=request.ameba_id,
            iterations=request.iterations,
        )

        if result["success"]:
            # Convert movements back to Pydantic models
            movements = []
            for movement in result["movements"]:
                movements.append(
                    MovementResult(
                        ameba_position=Position(
                            row=movement.ameba_position[0],
                            column=movement.ameba_position[1],
                        ),
                        old_position=Position(
                            row=movement.old_position[0],
                            column=movement.old_position[1],
                        ),
                        new_position=Position(
                            row=movement.new_position[0],
                            column=movement.new_position[1],
                        ),
                        energy_change=movement.energy_change,
                        food_consumed=(
                            Position(
                                row=movement.food_consumed[0],
                                column=movement.food_consumed[1],
                            )
                            if movement.food_consumed
                            else None
                        ),
                    )
                )

            # Convert game state back to Pydantic model
            updated_game_state = None
            if result.get("updated_game_state"):
                state = result["updated_game_state"]
                updated_game_state = GameState(
                    amebas=[
                        CellEntity(
                            type=ameba["type"],
                            energy=ameba["energy"],
                            position=Position(
                                row=ameba["position"]["row"],
                                column=ameba["position"]["column"],
                            ),
                        )
                        for ameba in state["amebas"]
                    ],
                    foods=[
                        CellEntity(
                            type=food["type"],
                            energy=food["energy"],
                            position=Position(
                                row=food["position"]["row"],
                                column=food["position"]["column"],
                            ),
                        )
                        for food in state["foods"]
                    ],
                    board_size=state["board_size"],
                )

            # Process food generation info
            food_generation = None
            if result.get("food_generation"):
                fg = result["food_generation"]
                food_generation = FoodGenerationInfo(
                    total_foods_consumed=fg.get("total_foods_consumed", 0),
                    total_foods_generated=fg.get("total_foods_generated", 0),
                    net_food_change=fg.get("net_food_change", 0),
                )

            return MoveResponse(
                success=result["success"],
                message=result["message"],
                movements=movements,
                updated_game_state=updated_game_state,
                iterations_completed=result["iterations_completed"],
                food_generation=food_generation,
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Movement failed: {result.get('error_details', result['message'])}",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Movement failed: {str(e)}")


@router.post("/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """
    Run a full game simulation

    - **iterations**: Number of simulation steps (1-1000)
    - **return_steps**: Whether to return intermediate steps (default: False)
    """
    try:
        # Use the movement handler for simulation
        result = movement_handler.run_simulation(
            iterations=request.iterations, return_steps=request.return_steps
        )

        if result["success"]:
            # Convert final game state to Pydantic model
            final_state = result["final_game_state"]
            final_game_state = GameState(
                amebas=[
                    CellEntity(
                        type=ameba["type"],
                        energy=ameba["energy"],
                        position=Position(
                            row=ameba["position"]["row"],
                            column=ameba["position"]["column"],
                        ),
                    )
                    for ameba in final_state["amebas"]
                ],
                foods=[
                    CellEntity(
                        type=food["type"],
                        energy=food["energy"],
                        position=Position(
                            row=food["position"]["row"],
                            column=food["position"]["column"],
                        ),
                    )
                    for food in final_state["foods"]
                ],
                board_size=final_state["board_size"],
            )

            # Convert steps if requested
            steps = None
            if request.return_steps and result.get("steps"):
                from movement.models import SimulationStep

                steps = []
                for step_data in result["steps"]:
                    step_movements = []
                    for movement in step_data["movements"]:
                        step_movements.append(
                            MovementResult(
                                ameba_position=Position(
                                    row=movement["ameba_position"]["row"],
                                    column=movement["ameba_position"]["column"],
                                ),
                                old_position=Position(
                                    row=movement["old_position"]["row"],
                                    column=movement["old_position"]["column"],
                                ),
                                new_position=Position(
                                    row=movement["new_position"]["row"],
                                    column=movement["new_position"]["column"],
                                ),
                                energy_change=movement["energy_change"],
                                food_consumed=(
                                    Position(
                                        row=movement["food_consumed"]["row"],
                                        column=movement["food_consumed"]["column"],
                                    )
                                    if movement["food_consumed"]
                                    else None
                                ),
                            )
                        )

                    step_state = step_data["game_state"]
                    step_game_state = GameState(
                        amebas=[
                            CellEntity(
                                type=ameba["type"],
                                energy=ameba["energy"],
                                position=Position(
                                    row=ameba["position"]["row"],
                                    column=ameba["position"]["column"],
                                ),
                            )
                            for ameba in step_state["amebas"]
                        ],
                        foods=[
                            CellEntity(
                                type=food["type"],
                                energy=food["energy"],
                                position=Position(
                                    row=food["position"]["row"],
                                    column=food["position"]["column"],
                                ),
                            )
                            for food in step_state["foods"]
                        ],
                        board_size=step_state["board_size"],
                    )

                    steps.append(
                        SimulationStep(
                            step_number=step_data["step_number"],
                            movements=step_movements,
                            game_state=step_game_state,
                            total_energy=step_data["total_energy"],
                        )
                    )

            return SimulationResponse(
                success=result["success"],
                message=result["message"],
                total_iterations=result["total_iterations"],
                final_game_state=final_game_state,
                steps=steps,
                statistics=result["statistics"],
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Simulation failed: {result.get('error_details', result['message'])}",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@router.get("/status")
async def get_movement_status():
    """Get the current movement system status"""
    try:
        # Check if game is loaded and ready
        game_loaded = movement_handler.game is not None

        if game_loaded:
            current_state = movement_handler._get_current_game_state()
            return {
                "game_loaded": True,
                "ameba_count": len(current_state["amebas"]),
                "food_count": len(current_state["foods"]),
                "board_size": current_state["board_size"],
                "message": "Movement system ready",
            }
        else:
            return {
                "game_loaded": False,
                "ameba_count": 0,
                "food_count": 0,
                "board_size": {"rows": 0, "columns": 0},
                "message": "Game not loaded - check configuration",
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get movement status: {str(e)}"
        )
