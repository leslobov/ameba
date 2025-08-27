from .play_desk_config import PlayDeskConfig
from .ameba import Ameba
from .position import Position

class PlayDesk:
    def __init__(self, config: PlayDeskConfig):
        self._width = config.width
        self._height = config.height
        self.amebas = []
        self.food_positions = []

    def generate_food(self):
        pass

    def get_total_energy(self) -> float:
        pass

    def get_visible_area(self, position: Position):
        pass  # Should return (list of Position, list of Ameba)