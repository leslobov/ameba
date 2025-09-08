from typing import Union

from src.abstract_classes.energy_item import EnergyItem
from src.abstract_classes.position_item import PositionItem


DeskEntity = Union[EnergyItem, PositionItem]
