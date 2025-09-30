import enum

from core.neural_network.models.base import BaseNeuralNetwork


class NeuralNetworkType(enum.IntEnum):
    BASE_NN = 1


def get_neural_network(type: NeuralNetworkType):
    if type == NeuralNetworkType.BASE_NN:
        return BaseNeuralNetwork
    raise ValueError(f"Unknown neural network type: {type}")
