from dataclasses import dataclass
from .play_desk_config import PlayDeskConfig
from .ameba_config import AmebaConfig

@dataclass
class GameConfig:
    total_energy: float
    play_desk: PlayDeskConfig
    ameba: AmebaConfig

    @staticmethod
    def from_dict(config_data: dict) -> "GameConfig":
        play_desk = PlayDeskConfig.from_dict(config_data["play_desk"])
        ameba = AmebaConfig.from_dict(config_data["ameba"])
        return GameConfig(
            total_energy=config_data["total_energy"],
            play_desk=play_desk,
            ameba=ameba,
        )