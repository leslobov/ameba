from dataclasses import dataclass

@dataclass
class PlayDeskConfig:
    width: int
    height: int

    @classmethod
    def from_dict(cls, data: dict) -> "PlayDeskConfig":
        return cls(
            width=data["width"],
            height=data["height"],
        )