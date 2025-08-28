from dataclasses import dataclass

@dataclass
class PlayDeskConfig:
    width: int
    height: int
    total_energy: float
    energy_per_food: float

    @classmethod
    def from_dict(cls, data: dict) -> "PlayDeskConfig":
        return cls(
            width=data["width"],
            height=data["height"],
            total_energy=data["total_energy"],
            energy_per_food=data["energy_per_food"],
        )