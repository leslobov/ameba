import json

from src.ameba import Ameba
from src.shared.visible_area import CalculateVisibleAreaService
from src.config_classes.game_config import GameConfig
from src.play_desk import PlayDesk

from src.neural_network.factory import NeuralNetworkType, get_neural_network


class Game:
    def __init__(self, config: GameConfig):
        self.config = config
        calculate_visible_area = CalculateVisibleAreaService(
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
        neural_network = get_neural_network(NeuralNetworkType.BASE_NN)(
            self.config.neural_network
        )
        return Ameba(
            self.config.ameba,
            position,
            energy,
            neural_network,
        )
