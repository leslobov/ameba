from src.abstract_classes.energy_item import EnergyItem
from src.abstract_classes.position_item import PositionItem
from src.shared_classes.position import Position


class Food(EnergyItem, PositionItem):
    def __init__(self, energy: float, position: Position):
        self._energy = energy
        self._position = position
        self._is_deleted = False

    def mark_deleted(self):
        self._is_deleted = True

    def get_energy(self) -> float:
        return self._energy

    def get_position(self) -> Position:
        return self._position

    def is_deleted(self) -> bool:
        return self._is_deleted
