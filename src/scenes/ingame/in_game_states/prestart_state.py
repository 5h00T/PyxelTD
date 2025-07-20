"""
ゲーム開始前（待機状態）のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scenes.in_game_scene import InGameScene
    from game import Game
    from input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
from .in_game_state import GameStateProtocol


class PreStartState(GameStateProtocol):
    """
    ゲーム開始前の待機状態。
    スタート入力でPlayingStateへ遷移。
    """

    def update(self, state_manager: "InGameStateManager", game: "Game", input_manager: "InputManager") -> None:
        # スペースキーでゲーム開始
        import pyxel

        if input_manager.is_triggered(pyxel.KEY_SPACE):
            state_manager.change_state(state_manager.playing_state)

    def draw(self, scene: "InGameScene", game: "Game") -> None:
        # 画面中央に「Press SPACE to Start」表示
        scene.draw_text_center("Press SPACE to Start", y=60)
