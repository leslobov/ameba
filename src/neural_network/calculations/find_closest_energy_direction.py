import torch


def find_closest_food_position(
    visible_area_energy_tensor: torch.Tensor,
) -> tuple[int, int] | None:
    rows, cols = visible_area_energy_tensor.shape
    center_row, center_column = rows // 2, cols // 2
    min_distance = float("inf")
    closest_food_position = None

    for i in range(rows):
        for j in range(cols):
            if visible_area_energy_tensor[i, j] > 0:
                distance = abs(i - center_row) + abs(j - center_column)
                if distance < min_distance:
                    min_distance = distance
                    closest_food_position = (i - center_row, j - center_column)

    return closest_food_position


def closest_energy_direction(visible_area_energy_tensor: torch.Tensor) -> torch.Tensor:
    closest_food_position = find_closest_food_position(visible_area_energy_tensor)
    if closest_food_position is None:
        return torch.tensor([0.25, 0.25, 0.25, 0.25], dtype=torch.float32)
    x, y = closest_food_position
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
