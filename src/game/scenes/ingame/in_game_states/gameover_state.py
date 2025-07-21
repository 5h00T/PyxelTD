"""
ゲームオーバー時のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol
from .state_result import StateResult


class GameOverState(GameStateProtocol):
    """
    ゲームオーバー状態。
    リトライやタイトルへの遷移を管理。
    """

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> StateResult:
        """
        Handle input during the game over state.
        R: Retry (restart current stage)
        Q: Return to menu
        """

        import pyxel

        result = StateResult.NONE
        if input_manager.is_triggered(pyxel.KEY_R):
            # リトライ: 現在のステージで再スタート
            result = StateResult.RETRY
        elif input_manager.is_triggered(pyxel.KEY_Q):
            # メニューに戻る
            result = StateResult.STAGE_SELECT

        return result

    def draw(self, manager: "InGameManager") -> None:
        """
        ゲームオーバー画面の描画。
        """
        import pyxel

        manager.map.draw()
        # 画面中央にゲームオーバー表示
        pyxel.text(60, 40, "GAME OVER", 8)
        pyxel.text(40, 60, "R: Retry   Q: Menu", 7)
