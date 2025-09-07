from typing import Optional, Sequence

from src.abstract_classes.energy_item import EnergyItem
from src.shared_classes.position import Position
from src.types.desk_entity import DeskEntity
from src.calculations.get_entity_by_position import find_entity_by_position


class VisibleEntities:
    def __init__(self, area: list[list[Optional[DeskEntity]]]):
        self._area = area

    def get_area(self) -> list[list[Optional[DeskEntity]]]:
        return self._area

    def get_visible_energy(self) -> list[list[float]]:
        energy_area = []
        for row in self._area:
            energy_row = []
            for entity in row:
                if isinstance(entity, EnergyItem):
                    energy_row.append(entity.get_energy())
                else:
                    energy_row.append(0)
            energy_area.append(energy_row)
        return energy_area

    def get_entity_on_position(self, position: Position) -> Optional[DeskEntity]:
        row = position.row + len(self._area) // 2
        column = position.column + len(self._area[0]) // 2
        if 0 <= row < len(self._area) and 0 <= column < len(self._area[0]):
            return self._area[row][column]
        return None


class CalculateVisibleArea:
    def __init__(
        self, visible_rows: int, visible_columns: int, desk_rows: int, desk_columns: int
    ):
        self._visible_rows = visible_rows
        self._visible_columns = visible_columns
        self._desk_rows = desk_rows
        self._desk_columns = desk_columns

    def fetch_visible_entities(
        self,
        reference_position: Position,
        fetched_entities: Sequence[DeskEntity],
    ) -> VisibleEntities:
        visible_entity_area = []
        for i in range(-self._visible_rows, self._visible_rows + 1):
            visible_entity_row = []
            for j in range(-self._visible_columns, self._visible_columns + 1):
                current_position = Position(
                    reference_position.row + i,
                    reference_position.column + j,
                )
                current_position.adjust_position(self._desk_rows, self._desk_columns)
                entity: Optional[DeskEntity] = find_entity_by_position(
                    current_position, fetched_entities
                )
                if entity is not None:
                    visible_entity_row.append(entity)
                else:
                    visible_entity_row.append(None)
            visible_entity_area.append(visible_entity_row)
        return VisibleEntities(visible_entity_area)
