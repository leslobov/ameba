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

from src.neural_network.calculations.find_closest_energy_direction import (
    closest_energy_direction,
)
from src.config_classes.neural_network_config import NeuralNetworkConfig
from src.shared.visible_area import VisibleEntities
from src.neural_network.abstract_classes.neural_network_model import NeuralNetwork


class BaseNeuralNetwork(NeuralNetwork):

    def __init__(self, config: NeuralNetworkConfig):
        net_state_path = os.path.join(
            os.path.dirname(__file__), "../net_state/base.pth"
        )
        self._generate_nn(config)
        if os.path.exists(net_state_path):
            self._nn.load_state_dict(torch.load(net_state_path))

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

    def train(self, steps: int, batch_size: int, mode: bool = True) -> None:
        self._nn.train(mode)
        criterion = nn.MSELoss()
        optimizer = torch.optim.SGD(self._nn.parameters(), lr=0.01)
        epochs = steps // batch_size

        batch_inputs = []
        batch_labels = []

        for _ in range(epochs):
            visible_energy_tensor = torch.zeros((11, 11), dtype=torch.float32)
            for _ in range(3):
                idx = torch.randint(0, visible_energy_tensor.shape[0], (2,))
                visible_energy_tensor[idx[0], idx[1]] = 1
            visible_energy_tensor[5, 5] = 0
            batch_inputs.append(torch.flatten(visible_energy_tensor))
            batch_labels.append(closest_energy_direction(visible_energy_tensor))

        inputs = torch.stack(batch_inputs)
        labels = torch.stack(batch_labels)

        batch_size = 64
        num_batches = inputs.size(0) // batch_size

        for epoch in range(epochs):
            for i in range(num_batches):
                batch_start = i * batch_size
                batch_end = batch_start + batch_size
                batch_inputs = inputs[batch_start:batch_end]
                batch_labels = labels[batch_start:batch_end]

                optimizer.zero_grad()
                outputs = self._nn(batch_inputs)
                loss = criterion(outputs, batch_labels)
                loss.backward()
                optimizer.step()

    def _generate_nn(self, config: NeuralNetworkConfig):
        self._neural_network_hidden_layers = config.initial_hidden_layers
        self._neurons_on_layer = config.initial_neurons_on_layer
        layers = []
        layers.append(nn.Linear(121, self._neurons_on_layer))
        layers.append(nn.Sigmoid())
        for _ in range(self._neural_network_hidden_layers - 1):
            layers.append(nn.Linear(self._neurons_on_layer, self._neurons_on_layer))
            layers.append(nn.Sigmoid())
        layers.append(nn.Linear(self._neurons_on_layer, 4))
        layers.append(nn.Softmax(dim=0))
        self._nn = nn.Sequential(*layers)


if __name__ == "__main__":

    config = NeuralNetworkConfig(initial_hidden_layers=2, initial_neurons_on_layer=32)
    neural_network = BaseNeuralNetwork(config)

    neural_network.train(100000, 64)
    net_state_path = os.path.join(os.path.dirname(__file__), "../net_state/base.pth")
    print(f"Saving neural network state to {net_state_path}")
    torch.save(neural_network._nn.state_dict(), net_state_path)
