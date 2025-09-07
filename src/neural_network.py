import torch
import torch.nn as nn
from torch.autograd import Function


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
        self.neural_network_hidden_layers = neural_network_hidden_layers
        self.neurons_on_layer = neurons_on_layer
        self.layers = self._create_layers()

    def _create_layers(self) -> nn.Sequential:
        layers = []
        for _ in range(self.neural_network_hidden_layers):
            layers.append(nn.Linear(self.neurons_on_layer, self.neurons_on_layer))
            layers.append(nn.Sigmoid())
        layers.append(nn.Linear(self.neurons_on_layer, 4))
        layers.append(nn.Softmax(dim=0))
        return nn.Sequential(*layers)

    def predict(self, x):
        # Pass the input through the neural network
        output = self.layers(x)

        # Get the predicted class
        predicted_class = torch.argmax(output, dim=0)

        return predicted_class

    def loss(self, prediction, target, lost_energy):
        return EnergyLoss().apply(prediction, target, lost_energy)

    def backpropagation(self, loss):
        loss.backward()
