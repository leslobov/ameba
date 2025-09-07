import unittest

from src.shared_classes.visible_area import CalculateVisibleArea
from src.play_desk import Position
from src.food import Food


class TestCalculateVisibleArea(unittest.TestCase):

    def test_fetch_visible_entities(self):
        calculate_visible_area = CalculateVisibleArea(
            visible_rows=2,
            visible_columns=2,
            desk_rows=7,
            desk_columns=7,
        )

        foods = [
            Food(energy=1, position=Position(1, 1)),
            Food(energy=2, position=Position(3, 3)),
            Food(energy=3, position=Position(2, 6)),
            Food(energy=4, position=Position(6, 0)),
        ]

        reference_position = Position(0, 1)

        expected_visible_energy = [
            [0, 0, 0, 0, 0],
            [0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [3, 0, 0, 0, 0],
        ]

        fetched_etities = calculate_visible_area.fetch_visible_entities(
            reference_position, foods
        )
        actual_visible_energy = fetched_etities.get_visible_energy()
        print(actual_visible_energy)
        self.assertEqual(actual_visible_energy, expected_visible_energy)
