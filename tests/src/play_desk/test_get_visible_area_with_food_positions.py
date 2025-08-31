import unittest
from unittest.mock import MagicMock
from src.play_desk import PlayDesk
from src.play_desk import Position
from src.play_desk import Ameba
from src.play_desk import PlayDeskConfig
from src.conf.ameba_config import AmebaConfig

class TestPlayDesk(unittest.TestCase):

    def test__get_visible_area_with_food_positions(self):
        config = PlayDeskConfig(width=7, height=7, total_energy=100, energy_per_food=5)
        play_desk = PlayDesk(config)

        ameba_config = AmebaConfig(neural_network_hidden_layers=2, 
                                    neurons_on_layer=5, 
                                    threhold_of_lostness_weight_coefficient=0.5, 
                                    visible_width=2, 
                                    visible_height=2, 
                                    initial_energy=50
        )
        ameba = Ameba(config=ameba_config, position=Position(0, 1), energy=50, neural_network=None)
        play_desk.amebas = [ameba]
        play_desk.food_positions = [Position(1, 1), Position(3, 3), Position(6, 0), Position(2, 6)]

        expected_area = [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0]
        ]
        actual_area = play_desk._get_visible_area_with_food_positions(ameba)
        self.assertEqual(actual_area, expected_area)
