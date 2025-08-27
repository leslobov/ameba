import os

from src.game import Game

def main():
    print("Welcome to Ameba Game!")
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    game = Game(Game.load_config(config_path))
    game.create_first_ameba()
    game.run(1000)

if __name__ == "__main__":
    main()