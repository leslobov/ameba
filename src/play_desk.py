import random

from .food import Food
from .conf.play_desk_config import PlayDeskConfig
from .ameba import Ameba
from .utils.position import Position

class PlayDesk:
    def __init__(self, config: PlayDeskConfig):
        self.config = config
        self.amebas = []
        self.foods = []

    def generate_food(self):
        used_energy = self._calculate_used_energy()
        available_energy = self.config.total_energy - used_energy
        added_energy = 0
        while added_energy < available_energy:
            energy = self.config.energy_per_food
            position = self.get_random_empty_position()
            food = Food(energy=energy, position=position)
            self.foods.append(food)
            added_energy += food.energy


    def get_random_empty_position(self) -> Position:
        while True:
            x = random.randint(0, self.config.width - 1)
            y = random.randint(0, self.config.height - 1)
            position = Position(x, y)
            if self._get_ameba_by_position(position):
                continue
            if self._get_food_by_position(position):
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
                food = self._get_food_by_position(line_positon)
                if food is not None:
                    visible_food_per_line.append(food.energy)
                else:
                    visible_food_per_line.append(0)
            visible_food_area.append(visible_food_per_line)
        return visible_food_area

    def _calculate_used_energy(self) -> float:
        food_energy = sum(food.energy for food in self.foods)
        ameba_energy = sum(ameba.energy for ameba in self.amebas)
        return food_energy + ameba_energy
    
    def _get_ameba_by_position(self, position: Position) -> bool:
        for ameba in self.amebas:
            if ameba.position.row == position.row and ameba.position.column == position.column:
                return ameba
        return None

    def _get_food_by_position(self, position: Position) -> bool:
        for food in self.foods:
            if food.position.row == position.row and food.position.column == position.column:
                return food
        return None

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
    