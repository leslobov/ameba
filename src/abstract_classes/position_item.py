from abc import ABC, abstractmethod

from src.shared_classes.position import Position


class PositionItem(ABC):
    @abstractmethod
    def get_position(self) -> Position:
        pass
