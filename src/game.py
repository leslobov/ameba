from .game_config import GameConfig
from .play_desk import PlayDesk

class Game:
    def __init__(self, config: GameConfig):
        self.play_desk = PlayDesk(config.play_desk)

    @staticmethod
    def load_config() -> GameConfig:
        pass

    def create_first_ameba(self):
        pass

    def run(self):
        pass

    def do_one_step(self):
        pass

    def get_info(self):
        pass