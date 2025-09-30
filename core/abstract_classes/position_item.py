from abc import ABC, abstractmethod

from core.shared.position import Position


class PositionItem(ABC):
    @abstractmethod
    def get_position(self) -> Position:
        pass
