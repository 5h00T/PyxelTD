"""
ゲームクリア時のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol
from .state_result import StateResult
from ....utils.font_renderer import FontRenderer


class ClearState(GameStateProtocol):
    """
    ゲームクリア状態。
    リザルトや次ステージへの遷移を管理。
    """

    def setup(self) -> None:
        """
        状態の初期化処理。
        必要に応じて実装する。
        """
        pass

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> StateResult:
        """
        ゲームクリア時の入力処理。
        Rキーでリトライ、Qキーでメニューに戻る。
        """
        import pyxel

        result = StateResult.NONE
        if input_manager.is_triggered(pyxel.KEY_Q):
            result = StateResult.STAGE_SELECT

        return result

    def draw(self, manager: "InGameManager") -> None:
        """
        ゲームクリア画面の描画。
        """
        font_renderer = FontRenderer.get_instance()
        font_renderer.draw_text(60, 40, "GAME CLEAR", 15, font_name="default")
        font_renderer.draw_text(60, 60, "Q: Menu", 15, font_name="default")
