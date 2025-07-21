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
        goal_enemies = self.enemy_manager.update()
        if goal_enemies:
            print(f"Goal reached by {len(goal_enemies)} enemies!")
            manager.base_hp -= len(goal_enemies)
            # ゴール到達エネミーはリストから除去
            self.enemy_manager.enemies = [e for e in self.enemy_manager.enemies if not (e.is_goal() and e.is_alive)]
            if manager.base_hp <= 0:
                # ゲームオーバー遷移
                state_manager.change_state(state_manager.gameover_state)

    def draw(self, manager: "InGameManager") -> None:
        """
        マップの描写を行う。
        """
        # manager.map.draw()
