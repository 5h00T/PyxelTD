"""
ゲームプレイ中のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol
from ..enemy.enemy_manager import EnemyManager


class PlayingState(GameStateProtocol):
    """
    ゲームプレイ中の状態。
    クリア・ゲームオーバー判定で状態遷移。
    """

    def __init__(self, enemy_manager: "EnemyManager") -> None:
        """
        初期化処理。
        必要な変数や状態を設定。
        """
        self.enemy_manager = enemy_manager

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> None:
        self.enemy_manager.update()

    def draw(self, manager: "InGameManager") -> None:
        """
        マップの描写を行う。
        """
        # manager.map.draw()
