import random

from src.calculations.get_entity_by_position import get_entity_by_position
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
            if get_entity_by_position(position, self._amebas) is not None:
                continue
            if get_entity_by_position(position, self._foods) is not None:
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
            print(
                "Ameba position: row= ",
                ameba._position.row,
                " col= ",
                ameba._position.column,
            )
        self._cleanup_play_desk()

    # def _get_visible_area_by_entities(
    #     self,
    #     ameba: Ameba,
    #     entities: Sequence[DeskEntity],
    #     func: Optional[Callable[[DeskEntity], T]] = None,
    # ) -> list[list[T]]:
    #     visible_entity_area = []
    #     for i in range(
    #         -ameba._config.visible_columns, ameba._config.visible_columns + 1
    #     ):
    #         visible_entity_per_line = []
    #         for j in range(-ameba._config.visible_rows, ameba._config.visible_rows + 1):
    #             position_on_line = Position(
    #                 ameba._position.row + i, ameba._position.column + j
    #             )
    #             position_on_line.adjust_position(self.config.rows, self.config.columns)
    #             entity: Optional[DeskEntity] = self._get_entity_by_position(
    #                 position_on_line, entities
    #             )
    #             if entity is not None:
    #                 if func is not None:
    #                     visible_entity_per_line.append(func(entity))
    #                 else:
    #                     visible_entity_per_line.append(entity)
    #             else:
    #                 visible_entity_per_line.append(0)
    #         visible_entity_area.append(visible_entity_per_line)
    #     return visible_entity_area

    def _calculate_used_energy(self) -> float:
        food_energy = sum(food.get_energy() for food in self._foods)
        ameba_energy = sum(ameba._energy for ameba in self._amebas)
        return food_energy + ameba_energy

    # def _get_entity_by_position(
    #     self, position: Position, entities: list[PositionEntity]
    # ) -> Optional[DeskEntity]:
    #     for entity in entities:
    #         if (
    #             entity.position.column == position.column
    #             and entity.position.row == position.row
    #         ):
    #             return entity
    #     return None

    def _cleanup_play_desk(self):
        self._foods = [food for food in self._foods if not food.is_deleted]
