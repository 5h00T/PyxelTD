"""
ゲームオーバー時のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol


class GameOverState(GameStateProtocol):
    """
    ゲームオーバー状態。
    リトライやタイトルへの遷移を管理。
    """

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> None:
        # エンターキーでタイトルへ戻る
        import pyxel

        if input_manager.is_triggered(pyxel.KEY_RETURN):
            manager.change_scene("title")

    def draw(self, manager: "InGameManager") -> None:
        """
        マップの描写を行う。
        """
        manager.map.draw()
