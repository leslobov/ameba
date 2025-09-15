import os
from typing import cast
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


def find_closest_food_position(
    visible_area_energy_tensor: torch.Tensor,
) -> tuple[int, int] | None:
    center_row, center_column = 5, 5
    min_distance = float("inf")
    closest_food_position = None

    for i in range(11):
        for j in range(11):
            if visible_area_energy_tensor[i * 11 + j] > 0:
                distance = abs(i - center_row) + abs(j - center_column)
                if distance < min_distance:
                    min_distance = distance
                    closest_food_position = (i - center_row, j - center_column)

    return closest_food_position


def calculate_optimal_move(moving_history: list[MoveSolution]) -> torch.Tensor:
    x, y = 0, 0
    for move_solution in moving_history:
        closest = find_closest_food_position(move_solution.visible_area_energy_tensor)
        if closest is not None:
            x += closest[0]
            y += closest[1]
            if abs(x) > abs(y):
                if x > 0:
                    return torch.tensor([0, 1, 0, 0], dtype=torch.float32)
                else:
                    return torch.tensor([0, 0, 0, 1], dtype=torch.float32)
            else:
                if y > 0:
                    return torch.tensor([1, 0, 0, 0], dtype=torch.float32)
                else:
                    return torch.tensor([0, 0, 1, 0], dtype=torch.float32)
        else:
            predicted_move = move_solution.predicted_move
            predicted_class = torch.argmax(predicted_move, dim=0).item()
            if predicted_class == 0:
                y += 1
            elif predicted_class == 1:
                x += 1
            elif predicted_class == 2:
                y -= 1
            elif predicted_class == 3:
                x -= 1


# def calculate_optimal_move_if_nothing_close(moving_history: list[MoveSolution]) -> torch.Tensor:
#     x, y = 0, 0
#     for move_solution in moving_history:
#         predicted_move = move_solution.predicted_move
#         predicted_class = torch.argmax(predicted_move, dim=0).item()
#         if predicted_class == 0:
#             y += 1
#         elif predicted_class == 1:
#             x += 1
#         elif predicted_class == 2:
#             y -= 1
#         elif predicted_class == 3:
#             x -= 1
#     if abs(x) > abs(y):
#         if x > 0:
#             return torch.tensor([0, 1, 0, 0], dtype=torch.float32)
#         else:
#             return torch.tensor([0, 0, 0, 1], dtype=torch.float32)
#     else:
#         if y > 0:
#             return torch.tensor([1, 0, 0, 0], dtype=torch.float32)
#         else:
#             return torch.tensor([0, 0, 1, 0], dtype=torch.float32)


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

    def predict(self, visible_entities: VisibleEntities) -> Number:

        visible_energy_tensor = torch.tensor(
            visible_entities.get_visible_energy(), dtype=torch.float32
        )

        flat_visible_energy_tensor = torch.flatten(visible_energy_tensor)
        output = self._layers(flat_visible_energy_tensor)
        self._append_moving_history(MoveSolution(flat_visible_energy_tensor, output))
        predicted_class = torch.argmax(output, dim=0)

        return predicted_class.item()

    def adjust_weights(self, energy_goal: float) -> None:
        self.train()
        self.zero_grad()
        steps = len(self._moving_history)
        for step in range(steps):
            move_solution = self._moving_history[step]
            optimal_move = calculate_optimal_move(self._moving_history[step:])
            predicted_move = self._layers(move_solution.visible_area_energy_tensor)
            creterion = nn.MSELoss()
            loss = creterion(predicted_move, optimal_move)
            self.zero_grad()
            loss.backward()
            print(f"Step {step+1}/{steps}, Loss: {loss.item()}")
            optimizer = torch.optim.SGD(self.parameters(), lr=0.01)
            optimizer.step()
        self._erase_moving_history()
        net_storage_path = os.path.join(os.path.dirname(__file__), "net.pth")
        torch.save(self.state_dict(), net_storage_path)

    def _create_layers(self) -> nn.Sequential:
        layers = []
        for _ in range(self._neural_network_hidden_layers):
            layers.append(nn.Linear(self._neurons_on_layer, self._neurons_on_layer))
            layers.append(nn.Sigmoid())
        layers.append(nn.Linear(self._neurons_on_layer, 4))
        layers.append(nn.Softmax(dim=0))
        return nn.Sequential(*layers)

    def _append_moving_history(self, move_solution: MoveSolution) -> None:
        self._moving_history.append(move_solution)

    def _erase_moving_history(self) -> None:
        self._moving_history = []
