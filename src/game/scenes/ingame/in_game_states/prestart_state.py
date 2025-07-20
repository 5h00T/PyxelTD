"""
ゲーム開始前（待機状態）のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol


class PreStartState(GameStateProtocol):
    """
    ゲーム開始前の待機状態。
    スタート入力でPlayingStateへ遷移。
    """

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> None:
        # スペースキーでゲーム開始
        import pyxel

        if input_manager.is_triggered(pyxel.KEY_SPACE):
            state_manager.change_state(state_manager.playing_state)

    def draw(self, manager: "InGameManager") -> None:
        """
        マップの描写を行う。
        """
        # manager.map.draw()
