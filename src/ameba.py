import torch

from src.shared_classes.visible_area import VisibleEntities
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
        self._is_daleted = False

    def get_energy(self) -> float:
        return self._energy

    def mark_deleted(self) -> None:
        self._is_deleted = True

    def is_deleted(self) -> bool:
        return self._is_deleted

    def get_position(self) -> Position:
        return self._position

    def move(self, visible_area: VisibleEntities) -> Position:
        prediction_item = self._neural_network.predict(visible_area)
        new_position = Position.move_according_prediction(prediction_item)
        entity_on_new_position = visible_area.get_entity_on_position(new_position)
        if entity_on_new_position is not None and isinstance(
            entity_on_new_position, EnergyItem
        ):
            self._eat_and_adjust_neural_network(entity_on_new_position)
        return new_position

    def _eat_and_adjust_neural_network(self, entity: EnergyItem):
        self._neural_network.adjust_weights(
            entity.get_energy(),
        )
        self._energy += entity.get_energy()
        entity.mark_deleted()

    def check_and_divide(self):
        pass  # Should return two Ameba instances

    def populate_history(self):
        pass

    def _get_visible_area_as_energy_tensor(
        self, visible_area: list[list[EnergyItem]]
    ) -> torch.Tensor:
        energy_area = []
        for row in visible_area:
            energy_row = []
            for entity in row:
                if isinstance(entity, float):
                    energy_row.append(entity.get_energy())
                else:
                    energy_row.append(0.0)
            energy_area.append(energy_row)
        return torch.tensor(energy_area, dtype=torch.float32)
