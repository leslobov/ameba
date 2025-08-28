import random
from .conf.play_desk_config import PlayDeskConfig
from .ameba import Ameba
from .utils.position import Position

class PlayDesk:
    def __init__(self, config: PlayDeskConfig):
        self.config = config
        self.amebas = []
        self.food_positions = []

    def generate_food(self):
        used_energy = self._caluclate_used_energy()
        available_energy = self.config.total_energy - used_energy
        added_energy = 0
        while added_energy < available_energy:
            position = self.get_random_empty_position()
            self.food_positions.append(position)
            added_energy += self.config.energy_per_food

    def get_visible_area(self, position: Position):
        pass  # Should return (list of Position, list of Ameba)

    def get_random_empty_position(self) -> Position:
        while True:
            x = random.randint(0, self.config.width - 1)
            y = random.randint(0, self.config.height - 1)
            position = Position(x, y)
            if self._is_position_occupied_by_ameba(position):
                continue
            if self._is_position_occupied_by_food(position):
                continue
            break
        return position
    
    def _caluclate_used_energy(self) -> float:
        food_energy = len(self.food_positions) * self.config.energy_per_food
        ameba_energy = sum(ameba.energy for ameba in self.amebas)
        return food_energy + ameba_energy
    
    def _is_position_occupied_by_ameba(self, position: Position) -> bool:
        for ameba in self.amebas:
            if ameba.position.x == position.x and ameba.position.y == position.y:
                return True
        return False
    
    def _is_position_occupied_by_food(self, position: Position) -> bool:
        for food in self.food_positions:
            if food.x == position.x and food.y == position.y:
                return True
        return False    
    
    def _get_position_by_delta(self, position: Position, delta_x: int, delta_y: int) -> Position:
        new_x = (position.x + delta_x) % self.config.width
        new_y = (position.y + delta_y) % self.config.height
        return Position(new_x, new_y)
    