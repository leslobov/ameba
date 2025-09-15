from dataclasses import dataclass

import torch


@dataclass
class MoveInfo:
    def __init__(
        self,
        visiible_area: torch.Tensor,
        visible_area_energy_tensor: torch.Tensor,
        predicted_move: torch.Tensor,
    ):
        self.visiible_area = visiible_area
        self.visible_area_energy_tensor = visible_area_energy_tensor
        self.predicted_move = predicted_move
