import sys
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.game import Game
from core.config_classes.game_config import GameConfig
from core.ameba import Ameba
from core.food import Food
from core.shared.position import Position as CorePosition


class MovementResult:
    def __init__(
        self,
        ameba_position: Tuple[int, int],
        old_position: Tuple[int, int],
        new_position: Tuple[int, int],
        energy_change: float = 0.0,
        food_consumed: Optional[Tuple[int, int]] = None,
    ):
        self.ameba_position = ameba_position
        self.old_position = old_position
        self.new_position = new_position
        self.energy_change = energy_change
        self.food_consumed = food_consumed


class GameState:
    def __init__(
        self, amebas: List[Dict], foods: List[Dict], board_size: Dict[str, int]
    ):
        self.amebas = amebas
        self.foods = foods
        self.board_size = board_size


class MovementHandler:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_path = project_root / "config.json"
        self.game = None
        self._load_game()

    def _load_game(self):
        """Load game configuration and initialize game"""
        try:
            if self.config_path.exists():
                config = Game.load_config(str(self.config_path))
                self.game = Game(config)
                self.game.initialize_play_desk()
            else:
                raise FileNotFoundError(f"Config file not found: {self.config_path}")
        except Exception as e:
            print(f"Error loading game: {e}")
            self.game = None

    def move_amebas(
        self,
        game_state: Optional[Dict] = None,
        ameba_id: Optional[int] = None,
        iterations: int = 1,
    ) -> Dict[str, Any]:
        """
        Move amebas on the game board

        Args:
            game_state: Optional custom game state, if None uses internal game state
            ameba_id: Optional specific ameba ID to move, if None moves all amebas
            iterations: Number of movement iterations

        Returns:
            Dictionary with movement results
        """
        try:
            if not self.game:
                return {
                    "success": False,
                    "message": "Game not initialized",
                    "movements": [],
                    "iterations_completed": 0,
                    "error_details": "Game configuration could not be loaded",
                }

            movements = []
            total_foods_consumed = 0
            total_foods_generated = 0

            # If custom game state provided, update internal state
            if game_state:
                self._update_game_state(game_state)

            # Perform movement iterations
            for iteration in range(iterations):
                iteration_result = self._do_single_move_iteration(ameba_id)
                movements.extend(iteration_result["movements"])
                total_foods_consumed += iteration_result["foods_consumed"]
                total_foods_generated += iteration_result["foods_generated"]

            # Get updated game state
            updated_state = self._get_current_game_state()

            # Create food generation info
            food_generation = {
                "total_foods_consumed": total_foods_consumed,
                "total_foods_generated": total_foods_generated,
                "net_food_change": total_foods_generated - total_foods_consumed,
            }

            return {
                "success": True,
                "message": f"Successfully completed {iterations} movement iteration(s)",
                "movements": movements,
                "updated_game_state": updated_state,
                "iterations_completed": iterations,
                "food_generation": food_generation,
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Movement failed: {str(e)}",
                "movements": [],
                "iterations_completed": 0,
                "error_details": str(e),
            }

    def _do_single_move_iteration(
        self, ameba_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Perform a single movement iteration"""
        movements = []

        if not self.game:
            return {
                "movements": movements,
                "foods_consumed": 0,
                "foods_generated": 0,
            }

        if ameba_id is not None:
            # Move specific ameba
            if ameba_id < len(self.game.play_desk._amebas):
                ameba = self.game.play_desk._amebas[ameba_id]
                movement = self._move_single_ameba(ameba, ameba_id)
                if movement:
                    movements.append(movement)
        else:
            # Move all amebas
            for i, ameba in enumerate(self.game.play_desk._amebas):
                movement = self._move_single_ameba(ameba, i)
                if movement:
                    movements.append(movement)

        # Cleanup and regenerate food
        food_count_before = len(
            [food for food in self.game.play_desk._foods if not food.is_deleted()]
        )
        self.game.play_desk._cleanup_play_desk()
        food_count_after_cleanup = len(
            [food for food in self.game.play_desk._foods if not food.is_deleted()]
        )

        # Original food generation
        self.game.play_desk.generate_food()
        food_count_after_generation = len(
            [food for food in self.game.play_desk._foods if not food.is_deleted()]
        )

        # Ensure minimum food count for gameplay
        minimum_foods = 12
        if food_count_after_generation < minimum_foods:
            foods_to_add = minimum_foods - food_count_after_generation
            print(
                f"[FOOD REGENERATION] Adding {foods_to_add} foods to reach minimum of {minimum_foods}"
            )

            from core.food import Food

            for _ in range(foods_to_add):
                try:
                    energy = self.game.config.play_desk.energy_per_food
                    position = self.game.play_desk.get_random_empty_position()
                    food = Food(energy=energy, position=position)
                    self.game.play_desk._foods.append(food)
                except Exception as e:
                    print(f"[FOOD REGENERATION] Error creating food: {e}")
                    break

            food_count_after_generation = len(
                [food for food in self.game.play_desk._foods if not food.is_deleted()]
            )

        # Calculate food statistics
        foods_consumed = food_count_before - food_count_after_cleanup
        foods_generated = food_count_after_generation - food_count_after_cleanup

        # Log food generation for debugging
        if foods_consumed > 0 or foods_generated > 0:
            print(
                f"[FOOD TRACKING] Before: {food_count_before}, After cleanup: {food_count_after_cleanup}, After generation: {food_count_after_generation}"
            )
            print(
                f"[FOOD TRACKING] Foods consumed: {foods_consumed}, Foods generated: {foods_generated}"
            )

        return {
            "movements": movements,
            "foods_consumed": foods_consumed,
            "foods_generated": foods_generated,
        }

    def _move_single_ameba(
        self, ameba: Ameba, ameba_id: int
    ) -> Optional[MovementResult]:
        """Move a single ameba and return movement result"""
        try:
            if not self.game:
                return None

            old_position = (ameba.get_position().row, ameba.get_position().column)
            old_energy = ameba.get_energy()

            # Get visible area and move ameba
            visible_area = self.game.play_desk._calculate_visible_area_service.fetch_visible_entities(
                ameba.get_position(), self.game.play_desk._foods
            )

            move_delta = ameba.move(visible_area)
            ameba._position += move_delta
            ameba._position.adjust_position(
                self.game.config.play_desk.rows, self.game.config.play_desk.columns
            )

            # Apply energy loss for movement (since core ameba.move doesn't do this)
            ameba._energy -= self.game.config.ameba.lost_energy_per_move

            new_position = (ameba.get_position().row, ameba.get_position().column)
            energy_change = ameba.get_energy() - old_energy

            # Check if food was consumed
            food_consumed = None
            if energy_change > 0:
                food_consumed = new_position

            return MovementResult(
                ameba_position=(ameba_id, ameba_id),  # Using ID as identifier
                old_position=old_position,
                new_position=new_position,
                energy_change=energy_change,
                food_consumed=food_consumed,
            )

        except Exception as e:
            print(f"Error moving ameba {ameba_id}: {e}")
            return None

    def _update_game_state(self, game_state: Dict):
        """Update internal game state from provided state"""
        # This would be implemented to sync external game state with internal state
        # For now, we'll work with the internal game state
        pass

    def _get_current_game_state(self) -> Dict[str, Any]:
        """Get current game state as dictionary"""
        if not self.game:
            return {"amebas": [], "foods": [], "board_size": {"rows": 0, "columns": 0}}

        amebas = []
        for i, ameba in enumerate(self.game.play_desk._amebas):
            if not ameba.is_deleted():
                amebas.append(
                    {
                        "type": "ameba",
                        "energy": ameba.get_energy(),
                        "position": {
                            "row": ameba.get_position().row,
                            "column": ameba.get_position().column,
                        },
                    }
                )

        foods = []
        for food in self.game.play_desk._foods:
            if not food.is_deleted():
                foods.append(
                    {
                        "type": "food",
                        "energy": food.get_energy(),
                        "position": {
                            "row": food.get_position().row,
                            "column": food.get_position().column,
                        },
                    }
                )

        return {
            "amebas": amebas,
            "foods": foods,
            "board_size": {
                "rows": self.game.config.play_desk.rows,
                "columns": self.game.config.play_desk.columns,
            },
        }

    def run_simulation(
        self, iterations: int, return_steps: bool = False
    ) -> Dict[str, Any]:
        """Run a full game simulation"""
        try:
            if not self.game:
                return {
                    "success": False,
                    "message": "Game not initialized",
                    "total_iterations": 0,
                    "final_game_state": {},
                    "error_details": "Game configuration could not be loaded",
                }

            steps = [] if return_steps else None

            for step in range(iterations):
                # Get state before movement
                if return_steps:
                    pre_state = self._get_current_game_state()

                # Do one step
                movements = self._do_single_move_iteration()

                # Record step if requested
                if return_steps and steps is not None:
                    post_state = self._get_current_game_state()
                    total_energy = sum(a["energy"] for a in post_state["amebas"]) + sum(
                        f["energy"] for f in post_state["foods"]
                    )

                    steps.append(
                        {
                            "step_number": step + 1,
                            "movements": [
                                {
                                    "ameba_position": {
                                        "row": m.ameba_position[0],
                                        "column": m.ameba_position[1],
                                    },
                                    "old_position": {
                                        "row": m.old_position[0],
                                        "column": m.old_position[1],
                                    },
                                    "new_position": {
                                        "row": m.new_position[0],
                                        "column": m.new_position[1],
                                    },
                                    "energy_change": m.energy_change,
                                    "food_consumed": (
                                        {
                                            "row": m.food_consumed[0],
                                            "column": m.food_consumed[1],
                                        }
                                        if m.food_consumed
                                        else None
                                    ),
                                }
                                for m in movements
                            ],
                            "game_state": post_state,
                            "total_energy": total_energy,
                        }
                    )

            final_state = self._get_current_game_state()
            total_energy = sum(a["energy"] for a in final_state["amebas"]) + sum(
                f["energy"] for f in final_state["foods"]
            )

            return {
                "success": True,
                "message": f"Simulation completed successfully with {iterations} iterations",
                "total_iterations": iterations,
                "final_game_state": final_state,
                "steps": steps,
                "statistics": {
                    "final_ameba_count": len(final_state["amebas"]),
                    "final_food_count": len(final_state["foods"]),
                    "total_energy": total_energy,
                },
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Simulation failed: {str(e)}",
                "total_iterations": 0,
                "final_game_state": {},
                "error_details": str(e),
            }
