import unittest
import torch
from core.neural_network.calculations.find_closest_energy_direction import (
    find_closest_food_position,
)


class TestFindClosestFoodPosition(unittest.TestCase):
    def setUp(self):
        self.size = 11
        self.center = (self.size // 2, self.size // 2)

    def test_no_food(self):
        tensor = torch.zeros((self.size, self.size), dtype=torch.float32)
        self.assertIsNone(find_closest_food_position(tensor))

    def test_food_at_center(self):
        tensor = torch.zeros((self.size, self.size), dtype=torch.float32)
        tensor[self.center] = 5
        self.assertEqual(find_closest_food_position(tensor), (0, 0))

    def test_food_at_top_left(self):
        tensor = torch.zeros((self.size, self.size), dtype=torch.float32)
        tensor[0, 0] = 3
        expected = (0 - self.center[0], 0 - self.center[1])
        self.assertEqual(find_closest_food_position(tensor), expected)

    def test_food_at_bottom_right(self):
        tensor = torch.zeros((self.size, self.size), dtype=torch.float32)
        tensor[self.size - 1, self.size - 1] = 2
        expected = (self.size - 1 - self.center[0], self.size - 1 - self.center[1])
        self.assertEqual(find_closest_food_position(tensor), expected)

    def test_multiple_food_closest(self):
        tensor = torch.zeros((self.size, self.size), dtype=torch.float32)
        tensor[0, 0] = 1
        tensor[self.center[0], self.center[1] + 1] = 2  # Closest to center
        expected = (0, 1)
        self.assertEqual(find_closest_food_position(tensor), expected)

    def test_multiple_food_same_distance(self):
        tensor = torch.zeros((self.size, self.size), dtype=torch.float32)
        tensor[self.center[0] - 1, self.center[1]] = 1
        tensor[self.center[0], self.center[1] + 1] = 1
        # Both are distance 1, but function will return the first found (row-wise)
        expected = (-1, 0)
        self.assertEqual(find_closest_food_position(tensor), expected)


if __name__ == "__main__":
    unittest.main()
