import random

from src.calculations.get_entity_by_position import find_entity_by_position
from src.shared_classes.visible_area import CalculateVisibleArea

from src.food import Food
from src.config_classes.play_desk_config import PlayDeskConfig
from src.ameba import Ameba
from src.shared_classes.position import Position


class PlayDesk:
    def __init__(
        self, config: PlayDeskConfig, calculate_visible_area: CalculateVisibleArea
    ):
        self._config = config
        self._amebas = list[Ameba]()
        self._foods = list[Food]()
        self._calculate_visible_area = calculate_visible_area

    def generate_food(self):
        used_energy = self._calculate_used_energy()
        available_energy = self._config.total_energy - used_energy
        added_energy = 0
        while added_energy < available_energy:
            energy = self._config.energy_per_food
            position = self.get_random_empty_position()
            food = Food(energy=energy, position=position)
            self._foods.append(food)
            added_energy += food.get_energy()

    def get_random_empty_position(self) -> Position:
        while True:
            row = random.randint(0, self._config.rows - 1)
            column = random.randint(0, self._config.columns - 1)
            position = Position(row, column)
            if find_entity_by_position(position, self._amebas) is not None:
                continue
            if find_entity_by_position(position, self._foods) is not None:
                continue
            break
        return position

    def do_move_amebas(self) -> None:
        for ameba in self._amebas:
            ameba._position += ameba.move(
                self._calculate_visible_area.fetch_visible_entities(
                    ameba.get_position(), self._foods
                )
            )
            ameba._position.adjust_position(self._config.rows, self._config.columns)
            print(
                "Ameba position: row= ",
                ameba._position.row,
                " col= ",
                ameba._position.column,
            )
        self._cleanup_play_desk()

    def _calculate_used_energy(self) -> float:
        food_energy = sum(food.get_energy() for food in self._foods)
        ameba_energy = sum(ameba._energy for ameba in self._amebas)
        return food_energy + ameba_energy

    def _cleanup_play_desk(self):
        self._foods = [food for food in self._foods if not food.is_deleted()]
