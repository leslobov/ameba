from .play_desk_config import PlayDeskConfig
from .ameba_config import AmebaConfig

class GameConfig:
    def __init__(self, total_energy: float, play_desk: PlayDeskConfig, ameba: AmebaConfig):
        self.total_energy = total_energy
        self.play_desk = play_desk
        self.ameba = ameba