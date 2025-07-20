"""
InGameStateManager - インゲームのステート管理クラス。
各状態インスタンスの生成・保持・遷移を一元管理。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ingame_manager import InGameManager
    from ....input_manager import InputManager
from .prestart_state import PreStartState
from .playing_state import PlayingState
from .clear_state import ClearState
from .gameover_state import GameOverState
from .in_game_state import GameStateProtocol
from ..enemy_manager import EnemyManager


class InGameStateManager:
    """
    インゲームのステート管理クラス。
    状態インスタンスの生成・保持・遷移を担当。
    """

    def __init__(self, enemy_manager: "EnemyManager") -> None:
        self.prestart_state = PreStartState()
        self.playing_state = PlayingState(enemy_manager)
        self.clear_state = ClearState()
        self.gameover_state = GameOverState()
        self.current_state: GameStateProtocol = self.prestart_state

    def change_state(self, new_state: GameStateProtocol) -> None:
        """
        状態を変更する。
        Args:
            new_state (GameStateProtocol): 新しい状態インスタンス
        """
        print(f"Changing state to {new_state.__class__.__name__}")
        self.current_state = new_state

    def update(self, manager: "InGameManager", input_manager: "InputManager") -> None:
        """
        現在の状態の更新処理。
        """
        self.current_state.update(self, manager, input_manager)

    def draw(self, manager: "InGameManager") -> None:
        """
        現在の状態の描画処理。
        """
        # ステートのdrawでmap描画が必要な場合はself.mapを参照可能
        self.current_state.draw(manager)
