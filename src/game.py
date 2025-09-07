import json

from src.ameba import Ameba
from src.neural_network import NeuralNetwork
from src.shared_classes.visible_area import CalculateVisibleArea

from src.config_classes.game_config import GameConfig
from src.play_desk import PlayDesk


class Game:
    def __init__(self, config: GameConfig):
        self.config = config
        calculate_visible_area = CalculateVisibleArea(
            visible_rows=config.ameba.visible_rows,
            visible_columns=config.ameba.visible_columns,
            desk_columns=config.play_desk.columns,
            desk_rows=config.play_desk.rows,
        )
        self.play_desk = PlayDesk(config.play_desk, calculate_visible_area)

    @staticmethod
    def load_config(config_path: str) -> GameConfig:
        with open(config_path, "r") as file_json:
            config_data = json.load(file_json)
        return GameConfig.from_dict(config_data)

    def initialize_play_desk(self):
        first_ameba = self._create_first_ameba()
        self.play_desk._amebas.append(first_ameba)
        self.play_desk.generate_food()

    def run(self, iterations: int):
        for _ in range(iterations):
            self.do_one_step()

    def do_one_step(self):
        self.play_desk.do_move_amebas()

    def get_info(self):
        pass

    def _create_first_ameba(self):
        position = self.play_desk.get_random_empty_position()
        energy = self.config.ameba.initial_energy
        neural_network = NeuralNetwork.generate_first_ameba_network(
            self.config.ameba.neural_network_hidden_layers,
            self.config.ameba.neurons_on_layer,
        )
        return Ameba(self.config.ameba, position, energy, neural_network)
