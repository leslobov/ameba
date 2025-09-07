import torch

from .utils.position import Position
from .conf.ameba_config import AmebaConfig
from .neural_network import NeuralNetwork
from .ameba_history import AmebaHistory


class Ameba:
    def __init__(
        self,
        config: AmebaConfig,
        position: Position,
        energy: float,
        neural_network: NeuralNetwork,
    ):
        self.config = config
        self.position = position
        self.energy = energy
        self.neural_network = neural_network
        self.history = []

    def move(self, visible_area):
        self.neural_network.eval()

        # Convert visible_area to a PyTorch tensor
        visible_area_tensor = torch.tensor(visible_area, dtype=torch.float32)

        # Flatten the tensor
        flat_visible_area = torch.flatten(visible_area_tensor)

        # Make a prediction
        with torch.no_grad():
            tensor_predict = self.neural_network.predict(flat_visible_area)

        return Position.move_according_prediction(tensor_predict.item())

    def check_and_divide(self):
        pass  # Should return two Ameba instances

    def eat_and_adjust_neural_network(self):
        pass

    def populate_history(self):
        pass
