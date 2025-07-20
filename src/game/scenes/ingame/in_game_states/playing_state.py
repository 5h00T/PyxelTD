"""
ゲームプレイ中のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol


class PlayingState(GameStateProtocol):
    """
    ゲームプレイ中の状態。
    クリア・ゲームオーバー判定で状態遷移。
    """

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> None:
        # TODO: ゲームロジック更新
        ...

    def draw(self, manager: "InGameManager") -> None:
        """
        マップの描写を行う。
        """
        # manager.map.draw()
