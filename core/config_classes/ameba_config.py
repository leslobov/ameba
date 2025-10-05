from dataclasses import dataclass


@dataclass
class AmebaConfig:
    threhold_of_lostness_weight_coefficient: float
    visible_rows: int
    visible_columns: int
    initial_energy: float
    lost_energy_per_move: float

    @classmethod
    def from_dict(cls, data: dict) -> "AmebaConfig":
        return cls(
            threhold_of_lostness_weight_coefficient=data[
                "threhold_of_lostness_weight_coefficient"
            ],
            visible_rows=data["visible_rows"],
            visible_columns=data["visible_columns"],
            initial_energy=data["initial_energy"],
            lost_energy_per_move=data["lost_energy_per_move"],
        )

    def to_dict(self) -> dict:
        return {
            "threhold_of_lostness_weight_coefficient": self.threhold_of_lostness_weight_coefficient,
            "visible_rows": self.visible_rows,
            "visible_columns": self.visible_columns,
            "initial_energy": self.initial_energy,
            "lost_energy_per_move": self.lost_energy_per_move,
        }
