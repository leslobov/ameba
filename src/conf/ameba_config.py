from dataclasses import dataclass


@dataclass
class AmebaConfig:
    neural_network_hidden_layers: int
    neurons_on_layer: int
    threhold_of_lostness_weight_coefficient: float
    visible_rows: int
    visible_columns: int
    initial_energy: float
    lost_energy_per_move: float

    @classmethod
    def from_dict(cls, data: dict) -> "AmebaConfig":
        return cls(
            neural_network_hidden_layers=data["neural_network_hidden_layers"],
            neurons_on_layer=data["neurons_on_layer"],
            threhold_of_lostness_weight_coefficient=data[
                "threhold_of_lostness_weight_coefficient"
            ],
            visible_rows=data["visible_rows"],
            visible_columns=data["visible_columns"],
            initial_energy=data["initial_energy"],
            lost_energy_per_move=data["lost_energy_per_move"],
        )

    @staticmethod
    def neurons_qnt_add():
        pass

    @staticmethod
    def energy_lost_per_move():
        pass
