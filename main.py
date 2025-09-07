import sys
import os

from src.game import Game

current_dir = os.path.dirname(os.path.abspath(__file__))

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


def main():
    print("Welcome to Ameba Game!")
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    game = Game(Game.load_config(config_path))
    game.initialize_play_desk()
    game.run(1)


if __name__ == "__main__":
    main()
