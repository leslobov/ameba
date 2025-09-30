import os
import torch
import torch.nn as nn
from torch.types import Number

from core.neural_network.calculations.find_closest_energy_direction import (
    closest_energy_direction,
)
from core.config_classes.neural_network_config import NeuralNetworkConfig
from core.shared.visible_area import VisibleEntities
from core.neural_network.abstract_classes.neural_network_model import NeuralNetwork


class BaseNeuralNetwork(NeuralNetwork):

    def __init__(self, config: NeuralNetworkConfig):
        self.config = config
        net_state_path = os.path.join(
            os.path.dirname(__file__), "../net_state/base.pth"
        )
        self._generate_nn()
        if os.path.exists(net_state_path):
            self._nn.load_state_dict(torch.load(net_state_path))

    def predict(self, visible_entities: VisibleEntities) -> Number:

        visible_energy_tensor = torch.tensor(
            visible_entities.get_visible_energy(), dtype=torch.float32
        )

        flat_visible_energy_tensor = torch.flatten(visible_energy_tensor)

        self._nn.eval()
        with torch.no_grad():
            output = self._nn(flat_visible_energy_tensor)
            print("Neural network output =", output)

        predicted_class = torch.argmax(output, dim=0)

        return predicted_class.item()

    def train(self, steps: int, batch_size: int, mode: bool = True) -> None:
        self._nn.train(mode)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self._nn.parameters(), lr=0.01)
        epochs = steps // batch_size

        batch_inputs = []
        batch_labels = []

        for _ in range(steps):
            visible_energy_tensor = torch.zeros((11, 11), dtype=torch.float32)
            num_points = int(torch.randint(1, 11, (1,)).item())
            for _ in range(num_points):
                idx = torch.randint(0, visible_energy_tensor.shape[0], (2,))
                visible_energy_tensor[idx[0], idx[1]] = 1
            visible_energy_tensor[5, 5] = 0
            batch_inputs.append(torch.flatten(visible_energy_tensor))
            batch_labels.append(closest_energy_direction(visible_energy_tensor))

        inputs = torch.stack(batch_inputs)
        labels = torch.stack(batch_labels)

        num_batches = inputs.size(0) // batch_size

        for epoch in range(epochs):
            running_loss = 0.0
            for i in range(num_batches):
                batch_start = i * batch_size
                batch_end = batch_start + batch_size
                batch_inputs = inputs[batch_start:batch_end]
                batch_labels = labels[batch_start:batch_end]

                outputs = self._nn(batch_inputs)
                loss = criterion(outputs, batch_labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

            avg_loss = running_loss / num_batches
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")

    def _generate_nn(self) -> None:
        self._neural_network_hidden_layers = self.config.initial_hidden_layers
        self._neurons_on_layer = self.config.initial_neurons_on_layer
        layers = []
        layers.append(nn.Linear(self.config.input_size, self._neurons_on_layer))
        layers.append(nn.ReLU())
        for _ in range(self._neural_network_hidden_layers):
            layers.append(nn.Linear(self._neurons_on_layer, self._neurons_on_layer))
            layers.append(nn.ReLU())
        layers.append(nn.Linear(self._neurons_on_layer, 4))
        self._nn = nn.Sequential(*layers)


if __name__ == "__main__":
    import json
    from core.config_classes.game_config import GameConfig

    config_path = os.path.join(os.environ["PROJECTPATH"], "config.json")
    with open(config_path, "r") as file_json:
        config_data = json.load(file_json)
    game_config = GameConfig.from_dict(config_data)

    neural_network = BaseNeuralNetwork(game_config.neural_network)

    neural_network.train(10000000, 6400)
    net_state_path = os.path.join(os.path.dirname(__file__), "../net_state/base.pth")
    print(f"Saving neural network state to {net_state_path}")
    torch.save(neural_network._nn.state_dict(), net_state_path)
