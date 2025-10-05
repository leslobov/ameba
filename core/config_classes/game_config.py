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

    def to_dict(self) -> dict:
        return {
            "play_desk": self.play_desk.to_dict(),
            "ameba": self.ameba.to_dict(),
            "neural_network": self.neural_network.to_dict(),
        }

    @classmethod
    def create_default(cls) -> "GameConfig":
        """Create a GameConfig with default values"""
        play_desk = PlayDeskConfig(
            rows=32, columns=32, total_energy=10000.0, energy_per_food=50.0
        )

        ameba = AmebaConfig(
            threhold_of_lostness_weight_coefficient=0.2,
            visible_rows=5,
            visible_columns=5,
            initial_energy=100.0,
            lost_energy_per_move=1.0,
        )

        # Calculate input size based on ameba visible area
        input_size = (2 * ameba.visible_rows + 1) * (2 * ameba.visible_columns + 1)

        neural_network = NeuralNetworkConfig(
            initial_hidden_layers=1, initial_neurons_on_layer=32, input_size=input_size
        )

        return cls(play_desk=play_desk, ameba=ameba, neural_network=neural_network)
