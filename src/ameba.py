from .utils.position import Position
from .conf.ameba_config import AmebaConfig
from .neural_network import NeuralNetwork
from .ameba_history import AmebaHistory

class Ameba:
    def __init__(self, position: Position, energy: float, neural_network: NeuralNetwork):
        self.position = position
        self.energy = energy
        self.neural_network = neural_network
        self.history = []

    def move(self):
        pass

    def check_and_divide(self):
        pass  # Should return two Ameba instances

    def eat_and_adjust_neural_network(self):
        pass

    def populate_history(self):
        pass