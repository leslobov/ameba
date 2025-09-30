import torch

from core.shared.visible_area import VisibleEntities
from core.abstract_classes.energy_item import EnergyItem
from core.abstract_classes.position_item import PositionItem

from core.shared.position import Position
from core.config_classes.ameba_config import AmebaConfig
from core.neural_network.abstract_classes.neural_network_model import NeuralNetwork


class Ameba(PositionItem, EnergyItem):
    def __init__(
        self,
        config: AmebaConfig,
        position: Position,
        energy: float,
        neutral_network: NeuralNetwork,
    ):
        self._config = config
        self._position = position
        self._energy = energy
        self._neural_network = neutral_network
        self._is_deleted = False

    def get_energy(self) -> float:
        return self._energy

    def mark_deleted(self) -> None:
        self._is_deleted = True

    def is_deleted(self) -> bool:
        return self._is_deleted

    def get_position(self) -> Position:
        return self._position

    def move(self, visible_area: VisibleEntities) -> Position:
        print("---------------init move------------------")
        print(
            "Ameba initial position: row= ",
            self._position.row,
            " col= ",
            self._position.column,
        )
        visible_energy = visible_area.get_visible_energy()
        print("visible_area.get_visible_energy() =")
        for i in range(len(visible_energy)):
            print(
                f"{i:02d} :",
                [
                    f"{j}: {visible_energy[i][j]:02.0f}"
                    for j in range(len(visible_energy[i]))
                ],
            )
        prediction_item = self._neural_network.predict(visible_area)
        print("prediction_item =", prediction_item)
        new_position = Position.move_according_prediction(prediction_item)
        print("new_position =", new_position.row, new_position.column)
        entity_on_new_position = visible_area.get_entity_on_position(new_position)
        if entity_on_new_position is not None and isinstance(
            entity_on_new_position, EnergyItem
        ):
            entity_on_new_position.mark_deleted()
            self._energy += entity_on_new_position.get_energy()
        print("+++++++++++++++ move end +++++++++++++++")
        return new_position

    def check_and_divide(self):
        pass  # Should return two Ameba instances

    def populate_history(self):
        pass
