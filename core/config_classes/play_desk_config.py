from dataclasses import dataclass


@dataclass
class PlayDeskConfig:
    rows: int
    columns: int
    total_energy: float
    energy_per_food: float

    @classmethod
    def from_dict(cls, data: dict) -> "PlayDeskConfig":
        return cls(
            rows=data["rows"],
            columns=data["columns"],
            total_energy=data["total_energy"],
            energy_per_food=data["energy_per_food"],
        )
