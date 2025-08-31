from src.utils.position import Position

class Food:
    def __init__(self, energy: float, position: Position):
        self.energy = energy
        self.position = position