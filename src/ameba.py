import torch

from src.abstract_classes.energy_item import EnergyItem
from src.abstract_classes.position_item import PositionItem

from src.shared_classes.position import Position
from src.config_classes.ameba_config import AmebaConfig
from src.neural_network import NeuralNetwork


class Ameba(PositionItem, EnergyItem):
    def __init__(
        self,
        config: AmebaConfig,
        position: Position,
        energy: float,
        neural_network: NeuralNetwork,
    ):
        self._config = config
        self._position = position
        self._energy = energy
        self._neural_network = neural_network
        self._history = []

    def move(self, visible_area):
        self._neural_network.eval()

        # Convert visible_area to a PyTorch tensor
        visible_area_tensor = torch.tensor(
            visible_area.get_visible_energy(), dtype=torch.float32
        )

        # Flatten the tensor
        flat_visible_area_tensor = torch.flatten(visible_area_tensor)

        # Make a prediction
        with torch.no_grad():
            tensor_predict = self._neural_network.predict(flat_visible_area_tensor)

        new_position = Position.move_according_prediction(tensor_predict.item())
        return new_position

    def check_and_divide(self):
        pass  # Should return two Ameba instances

    def eat_and_adjust_neural_network(self):
        pass

    def populate_history(self):
        pass

    def get_energy(self) -> float:
        return self._energy

    def get_position(self) -> Position:
        return self._position

    def _get_visible_area_as_energy_tensor(
        self, visible_area: list[list[EnergyItem]]
    ) -> torch.Tensor:
        energy_area = []
        for row in visible_area:
            energy_row = []
            for entity in row:
                if isinstance(entity, float):
                    energy_row.append(entity)
                else:
                    energy_row.append(0.0)
            energy_area.append(energy_row)
        return torch.tensor(energy_area, dtype=torch.float32)
