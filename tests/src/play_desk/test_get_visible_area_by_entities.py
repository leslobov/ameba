import unittest
from src.neural_network import NeuralNetwork
from src.play_desk import PlayDesk
from src.play_desk import Position
from src.play_desk import Ameba
from src.play_desk import PlayDeskConfig
from src.conf.ameba_config import AmebaConfig
from src.food import Food


class TestPlayDesk(unittest.TestCase):

    def test__get_visible_area_by_entities(self):
        config = PlayDeskConfig(columns=7, rows=7, total_energy=100, energy_per_food=5)
        play_desk = PlayDesk(config)

        ameba_config = AmebaConfig(
            neural_network_hidden_layers=2,
            neurons_on_layer=5,
            threhold_of_lostness_weight_coefficient=0.5,
            visible_rows=2,
            visible_columns=2,
            initial_energy=50,
        )
        ameba = Ameba(
            config=ameba_config,
            position=Position(0, 1),
            energy=50,
            neural_network=NeuralNetwork([]),
        )
        play_desk.amebas = [ameba]
        play_desk.foods = [
            Food(energy=1, position=Position(1, 1)),
            Food(energy=2, position=Position(3, 3)),
            Food(energy=3, position=Position(2, 6)),
            Food(energy=4, position=Position(6, 0)),
        ]

        expected_area = [
            [0, 0, 0, 0, 0],
            [0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [3, 0, 0, 0, 0],
        ]
        actual_area = play_desk._get_visible_area_by_entities(
            ameba, play_desk.foods, lambda food: food.energy
        )
        self.assertEqual(actual_area, expected_area)
