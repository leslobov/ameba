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

    def _get_visible_area_with_food_positions(self, ameba: Ameba):
        visible_food_area = []
        for i in range(-ameba.config.visible_height, ameba.config.visible_height +1):
            visible_food_per_line = []
            for j in range(-ameba.config.visible_width, ameba.config.visible_width + 1):
                line_positon = Position(ameba.position.row + i, ameba.position.column + j)
                line_positon = self._recalculate_position(line_positon)
                if (self._is_position_occupied_by_food(line_positon)):
                    visible_food_per_line.append(1)
                else:
                    visible_food_per_line.append(0)
            visible_food_area.append(visible_food_per_line)
        return visible_food_area
    
    def _caluclate_used_energy(self) -> float:
        food_energy = len(self.food_positions) * self.config.energy_per_food
        ameba_energy = sum(ameba.energy for ameba in self.amebas)
        return food_energy + ameba_energy
    
    def _is_position_occupied_by_ameba(self, position: Position) -> bool:
        for ameba in self.amebas:
            if ameba.position.row == position.row and ameba.position.column == position.column:
                return True
        return False
    
    def _is_position_occupied_by_food(self, position: Position) -> bool:
        for food in self.food_positions:
            if food.row == position.row and food.column == position.column:
                return True
        return False

    def _recalculate_position(self, position: Position) -> Position:
        if position.row < 0:
            position.row += self.config.width
        if position.column < 0:
            position.column += self.config.height
        return position  
    
    def _get_position_by_delta(self, position: Position, delta_row: int, delta_column: int) -> Position:
        new_row = (position.row + delta_row) % self.config.width
        new_column = (position.column + delta_column) % self.config.height
        return Position(new_row, new_column)
    