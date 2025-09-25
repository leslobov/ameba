from dataclasses import dataclass

from .neural_network_config import NeuralNetworkConfig
from .play_desk_config import PlayDeskConfig
from .ameba_config import AmebaConfig


@dataclass
class GameConfig:
    play_desk: PlayDeskConfig
    ameba: AmebaConfig
    neural_network: NeuralNetworkConfig

    @staticmethod
    def from_dict(config_data: dict) -> "GameConfig":
        play_desk = PlayDeskConfig.from_dict(config_data["play_desk"])
        ameba = AmebaConfig.from_dict(config_data["ameba"])
        config_data["neural_network"]["input_size"] = (2 * ameba.visible_rows + 1) * (
            2 * ameba.visible_columns + 1
        )
        neural_network = NeuralNetworkConfig.from_dict(config_data["neural_network"])
        return GameConfig(
            play_desk=play_desk, ameba=ameba, neural_network=neural_network
        )
