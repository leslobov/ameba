import random

from .food import Food
from .conf.play_desk_config import PlayDeskConfig
from .ameba import Ameba
from .utils.position import Position
from typing import Sequence, Union, Optional, Callable, TypeVar

T = TypeVar("T")

DeskEntity = Union[Food, Ameba]


class PlayDesk:
    def __init__(self, config: PlayDeskConfig):
        self.config = config
        self.amebas = list[Ameba]()
        self.foods = list[Food]()

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
            row = random.randint(0, self.config.rows - 1)
            column = random.randint(0, self.config.columns - 1)
            position = Position(row, column)
            if self._get_entity_by_position(position, self.amebas) is not None:
                continue
            if self._get_entity_by_position(position, self.foods) is not None:
                continue
            break
        return position

    def do_move_amebas(self) -> None:
        for ameba in self.amebas:
            ameba.position += ameba.move(
                self._get_visible_area_by_entities(
                    ameba, self.foods, lambda food: food.energy
                )
            )
            food_under_ameba = self._get_entity_by_position(ameba.position, self.foods)
            if food_under_ameba is not None:
                ameba.energy += food_under_ameba.energy
                self.foods.remove(food_under_ameba)
                ameba.eat_and_adjust_neural_network()
            print(
                "Ameba position: row= ",
                ameba.position.row,
                " col= ",
                ameba.position.column,
            )

    def _get_visible_area_by_entities(
        self,
        ameba: Ameba,
        entities: Sequence[DeskEntity],
        func: Optional[Callable[[DeskEntity], T]],
    ) -> list[list[T]]:
        visible_entity_area = []
        for i in range(-ameba.config.visible_columns, ameba.config.visible_columns + 1):
            visible_entity_per_line = []
            for j in range(-ameba.config.visible_rows, ameba.config.visible_rows + 1):
                position_on_line = Position(
                    ameba.position.row + i, ameba.position.column + j
                )
                position_on_line.adjust_position(self.config.rows, self.config.columns)
                entity: Optional[DeskEntity] = self._get_entity_by_position(
                    position_on_line, entities
                )
                if entity is not None:
                    if func is not None:
                        visible_entity_per_line.append(func(entity))
                    else:
                        visible_entity_per_line.append(entity)
                else:
                    visible_entity_per_line.append(0)
            visible_entity_area.append(visible_entity_per_line)
        return visible_entity_area

    def _calculate_used_energy(self) -> float:
        food_energy = sum(food.energy for food in self.foods)
        ameba_energy = sum(ameba.energy for ameba in self.amebas)
        return food_energy + ameba_energy

    def _get_entity_by_position(
        self, position: Position, entities: T
    ) -> Optional[DeskEntity]:
        for entity in entities:
            if (
                entity.position.column == position.column
                and entity.position.row == position.row
            ):
                return entity
        return None
