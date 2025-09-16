import os
from typing_extensions import Self
import torch
import torch.nn as nn
from torch.types import Number

import sys

# TODO: remove this hack to import from src, use vscode settings instead
src_path = os.path.join(os.path.dirname(__file__), "..", "..", "..")
src_path = os.path.abspath(src_path)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from src.config_classes.neural_network_config import NeuralNetworkConfig
from src.shared.visible_area import VisibleEntities
from src.neural_network.abstract_classes.neural_network_model import NeuralNetwork


class BaseNeuralNetwork(NeuralNetwork):

    def __init__(self, config: NeuralNetworkConfig):
        net_state_path = os.path.join(os.path.dirname(__file__), "net_state/base.pth")
        if os.path.exists(net_state_path):
            self._nn.load_state_dict(torch.load(net_state_path))
        else:
            self._generate_nn(config)

    def predict(self, visible_entities: VisibleEntities) -> Number:

        # Convert visible_area to a PyTorch tensor
        visible_energy_tensor = torch.tensor(
            visible_entities.get_visible_energy(), dtype=torch.float32
        )

        # Flatten the tensor
        flat_visible_energy_tensor = torch.flatten(visible_energy_tensor)

        # Pass the input through the neural network
        self._nn.eval()
        with torch.no_grad():
            output = self._nn(flat_visible_energy_tensor)

        # Get the predicted class
        predicted_class = torch.argmax(output, dim=0)

        return predicted_class.item()

    def train(self, mode: bool = True) -> None:
        steps = 1000
        self._nn.train(mode)
        criterion = nn.MSELoss()
        optimizer = torch.optim.SGD(self._nn.parameters(), lr=0.01)
        optimizer.zero_grad()

        visible_energy_tensor = torch.zeros((11, 11), dtype=torch.float32)
        for i in range(3):
            idx = torch.randint(0, visible_energy_tensor.shape[0], (2,))
            visible_energy_tensor[idx[0], idx[1]] = 1
        visible_energy_tensor[5, 5] = 0
        print(visible_energy_tensor)

        for step in range(steps):
            pass
            # flat_visible_energy_tensor = torch.zeros(1, 121)
            # for i in range(3):
            #     idx = torch.randint(0, flat_visible_energy_tensor.shape[1], (1,))
            #     if idx.item() != 60:
            #         flat_visible_energy_tensor[0, idx] = 1
            # output = self._nn(flat_visible_energy_tensor)
            # target = torch.tensor([0.0, 0.0, 0.0, 0.0])

            # Forward pass
        # Dummy training loop (replace with actual training data)

    def _generate_nn(self, config: NeuralNetworkConfig):
        self._neural_network_hidden_layers = config.initial_hidden_layers
        self._neurons_on_layer = config.initial_neurons_on_layer
        layers = []
        for _ in range(self._neural_network_hidden_layers):
            layers.append(nn.Linear(self._neurons_on_layer, self._neurons_on_layer))
            layers.append(nn.Sigmoid())
        layers.append(nn.Linear(self._neurons_on_layer, 4))
        layers.append(nn.Softmax(dim=0))
        self._nn = nn.Sequential(*layers)


if __name__ == "__main__":

    config = NeuralNetworkConfig(
        initial_hidden_layers=3,
        initial_neurons_on_layer=121,
    )
    neural_network = BaseNeuralNetwork(config)

    neural_network.train()
