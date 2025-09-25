from dataclasses import dataclass


@dataclass
class NeuralNetworkConfig:
    initial_hidden_layers: int
    initial_neurons_on_layer: int
    input_size: int

    @classmethod
    def from_dict(cls, data: dict) -> "NeuralNetworkConfig":
        return cls(
            initial_hidden_layers=data["initial_hidden_layers"],
            initial_neurons_on_layer=data["initial_neurons_on_layer"],
            input_size=data["input_size"],
        )
