import json

from .game_config import GameConfig
from .play_desk import PlayDesk

class Game:
    def __init__(self, config: GameConfig):
        self.play_desk = PlayDesk(config.play_desk)

    @staticmethod
    def load_config(path_to_file) -> GameConfig:
        with open("config.json", "r") as file_json:
            config_data = json.load(file_json)
        return GameConfig.from_dict(config_data)

    def create_first_ameba(self):
        pass

    def run(self, iterations: int):
        
        pass

    def do_one_step(self):
        pass

    def get_info(self):
        pass