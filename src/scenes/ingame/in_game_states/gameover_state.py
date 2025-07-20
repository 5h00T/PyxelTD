"""
ゲームオーバー時のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scenes.in_game_scene import InGameScene
    from game import Game
    from input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
from .in_game_state import GameStateProtocol


class GameOverState(GameStateProtocol):
    """
    ゲームオーバー状態。
    リトライやタイトルへの遷移を管理。
    """

    def update(self, state_manager: "InGameStateManager", game: "Game", input_manager: "InputManager") -> None:
        # エンターキーでタイトルへ戻る
        import pyxel
        from scenes.title_scene import TitleScene

        if input_manager.is_triggered(pyxel.KEY_RETURN):
            game.change_scene(TitleScene())

    def draw(self, scene: "InGameScene", game: "Game") -> None:
        # 画面中央に「Game Over」表示
        scene.draw_text_center("Game Over", y=60)
