from dataclasses import dataclass
import torch
import torch.nn as nn
from torch.autograd import Function
from torch.types import Number

from src.shared_classes.visible_area import VisibleEntities


@dataclass
class MoveSolution:
    def __init__(
        self,
        visible_area_energy_tensor: torch.Tensor,
        predicted_move: torch.Tensor,
    ):
        self.visible_area_energy_tensor = visible_area_energy_tensor
        self.predicted_move = predicted_move


class EnergyLoss(Function):
    @staticmethod
    def forward(ctx, move_pred, move_true, lost_energy) -> float:
        ctx.save_for_backward(move_pred, move_true, lost_energy)
        return lost_energy**2

    @staticmethod
    def backward(ctx, grad_output: float) -> float:
        (move_pred, move_true, lost_energy) = ctx.saved_tensors
        grad_lost_energy = lost_energy * grad_output
        return grad_lost_energy


class NeuralNetwork(nn.Module):
    @staticmethod
    def generate_first_ameba_network(
        neural_network_hidden_layers: int, neurons_on_layer: int
    ):
        net = NeuralNetwork(neural_network_hidden_layers, neurons_on_layer)
        return net

    def __init__(self, neural_network_hidden_layers: int, neurons_on_layer: int):
        super(NeuralNetwork, self).__init__()
        self._neural_network_hidden_layers = neural_network_hidden_layers
        self._neurons_on_layer = neurons_on_layer
        self._layers = self._create_layers()
        self._moving_history: list[MoveSolution] = []

    def append_moving_history(self, move_solution: MoveSolution) -> None:
        self._moving_history.append(move_solution)

    def erase_moving_history(self) -> None:
        self._moving_history = []

    def adjust_weights(self, added_energy: float) -> None:
        pass
        # if not history_visible_energy_area_flatten_tensors:
        #     return

        # for visible_area_tensor in history_visible_energy_area_flatten_tensors:
        #     self.train()
        #     self.zero_grad()

        #     # Make a prediction
        #     prediction = self.predict(visible_area_tensor)

        #     # Assume the target is to move towards food (for simplicity, we use 0 as the target)
        #     target = torch.tensor(0)

        #     # Calculate lost energy (for simplicity, we use a constant value)
        #     lost_energy = torch.tensor(1.0, requires_grad=True)

        #     # Calculate loss
        #     loss = self.loss(prediction, target, lost_energy)

        #     # Backpropagation
        #     self.backpropagation(loss)

        #     # Update weights
        #     optimizer = torch.optim.SGD(self.parameters(), lr=0.01)
        #     optimizer.step()

    def _create_layers(self) -> nn.Sequential:
        layers = []
        for _ in range(self._neural_network_hidden_layers):
            layers.append(nn.Linear(self._neurons_on_layer, self._neurons_on_layer))
            layers.append(nn.Sigmoid())
        layers.append(nn.Linear(self._neurons_on_layer, 4))
        layers.append(nn.Softmax(dim=0))
        return nn.Sequential(*layers)

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
            output = self._layers(flat_visible_energy_tensor)

        # Get the predicted class
        predicted_class = torch.argmax(output, dim=0)

        return predicted_class.item()

    def loss(self, prediction, target, lost_energy):
        return EnergyLoss().apply(prediction, target, lost_energy)

    def backpropagation(self, loss):
        loss.backward()
