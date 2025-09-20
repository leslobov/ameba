import random

from src.calculations.get_entity_by_position import find_entity_by_position
from src.shared.visible_area import CalculateVisibleAreaService

from src.food import Food
from src.config_classes.play_desk_config import PlayDeskConfig
from src.ameba import Ameba
from src.shared.position import Position


class PlayDesk:
    def __init__(
        self,
        config: PlayDeskConfig,
        calculate_visible_area_service: CalculateVisibleAreaService,
    ):
        self._config = config
        self._amebas = list[Ameba]()
        self._foods = list[Food]()
        self._calculate_visible_area_service = calculate_visible_area_service

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
            move_position = ameba.move(
                self._calculate_visible_area_service.fetch_visible_entities(
                    ameba.get_position(), self._foods
                )
            )
            ameba._position += move_position
        self._cleanup_play_desk()
        self.generate_food()

    def _calculate_used_energy(self) -> float:
        food_energy = sum(food.get_energy() for food in self._foods)
        ameba_energy = sum(ameba._energy for ameba in self._amebas)
        return food_energy + ameba_energy

    def _cleanup_play_desk(self):
        self._foods = [food for food in self._foods if not food.is_deleted()]
