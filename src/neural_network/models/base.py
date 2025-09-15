import torch
import torch.nn as nn
from torch.types import Number

from src.config_classes.neural_network_config import NeuralNetworkConfig
from src.shared.visible_area import VisibleEntities
from src.neural_network.abstract_classes.neural_network_model import NeuralNetwork


class BaseNeuralNetwork(nn.Module, NeuralNetwork):

    def __init__(self, config: NeuralNetworkConfig):
        super().__init__()
        self._neural_network_hidden_layers = config.initial_hidden_layers
        self._neurons_on_layer = config.initial_neurons_on_layer
        self._layers = self._create_layers()

    def predict(self, visible_entities: VisibleEntities) -> Number:

        # Convert visible_area to a PyTorch tensor
        visible_energy_tensor = torch.tensor(
            visible_entities.get_visible_energy(), dtype=torch.float32
        )

        # Flatten the tensor
        flat_visible_energy_tensor = torch.flatten(visible_energy_tensor)

        # Pass the input through the neural network
        self.eval()
        with torch.no_grad():
            output = self.forward(flat_visible_energy_tensor)

        # Get the predicted class
        predicted_class = torch.argmax(output, dim=0)

        return predicted_class.item()

    def forward(self, flat_visible_energy_tensor: torch.Tensor) -> torch.Tensor:
        return self._layers(flat_visible_energy_tensor)

    def _create_layers(self) -> nn.Sequential:
        layers = []
        for _ in range(self._neural_network_hidden_layers):
            layers.append(nn.Linear(self._neurons_on_layer, self._neurons_on_layer))
            layers.append(nn.Sigmoid())
        layers.append(nn.Linear(self._neurons_on_layer, 4))
        layers.append(nn.Softmax(dim=0))
        return nn.Sequential(*layers)
