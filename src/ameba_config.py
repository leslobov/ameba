from dataclasses import dataclass

@dataclass
class AmebaConfig:
    neural_network_hidden_layers: int
    neurons_on_layer: int
    threhold_of_lostness_weight_coefficient: float
    visible_width: int
    visible_height: int
    initial_energy: float

    @classmethod
    def from_dict(cls, data: dict) -> "AmebaConfig":
        return cls(
            neural_network_hidden_layers=data["neural_network_hidden_layers"],
            neurons_on_layer=data["neurons_on_layer"],
            threhold_of_lostness_weight_coefficient=data["threhold_of_lostness_weight_coefficient"],
            visible_width=data["visible_width"],
            visible_height=data["visible_height"],
            initial_energy=data["initial_energy"]
        )

    @staticmethod
    def neurons_qnt_add():
        pass

    @staticmethod
    def energy_lost_per_move():
        pass