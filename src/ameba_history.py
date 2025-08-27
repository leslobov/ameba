from .position import Position

class AmebaHistory:
    def __init__(
        self,
        step: int,
        position: Position,
        energy: float,
        visible_food_positions: list,
        visible_ameba_positions: list,
    ):
        self.step = step
        self.position = position
        self.energy = energy
        self.visible_food_positions = visible_food_positions
        self.visible_ameba_positions = visible_ameba_positions