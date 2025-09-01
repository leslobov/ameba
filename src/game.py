import json

from src.ameba import Ameba
from src.neural_network import NeuralNetwork

from .conf.game_config import GameConfig
from .play_desk import PlayDesk


class Game:
    def __init__(self, config: GameConfig):
        self.config = config
        self.play_desk = PlayDesk(config.play_desk)

    @staticmethod
    def load_config(config_path: str) -> GameConfig:
        with open(config_path, "r") as file_json:
            config_data = json.load(file_json)
        return GameConfig.from_dict(config_data)

    def initialize_play_desk(self):
        first_ameba = self._create_first_ameba()
        self.play_desk.amebas.append(first_ameba)
        self.play_desk.generate_food()

    def run(self, iterations: int):
        self.initialize_play_desk()
        pass

    def do_one_step(self):
        pass

    def get_info(self):
        pass

    def _create_first_ameba(self):
        position = self.play_desk.get_random_empty_position()
        energy = self.config.ameba.initial_energy
        neural_network = NeuralNetwork.generate_first_ameba_network()
        return Ameba(self.config.ameba, position, energy, neural_network)
