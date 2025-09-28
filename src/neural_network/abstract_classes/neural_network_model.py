from abc import ABC, abstractmethod

from torch.types import Number

from src.config_classes.neural_network_config import NeuralNetworkConfig
from src.shared.visible_area import VisibleEntities


class NeuralNetwork(ABC):
    def __init__(self, config: NeuralNetworkConfig):
        pass

    @abstractmethod
    def predict(self, visible_entities: VisibleEntities) -> Number:
        pass

    @abstractmethod
    def train(self, steps: int, batch_size: int, mode: bool = True) -> None:
        pass
