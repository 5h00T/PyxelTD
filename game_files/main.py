"""
ゲーム起動用エントリポイント。
ゲームループ本体は game.py に記載。
"""

from src.game.game import Game

if __name__ == "__main__":
    game: Game = Game()
