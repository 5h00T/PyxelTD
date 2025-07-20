"""
InGameManager - インゲームのマップとステート管理を一元化するクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...game import Game
    from ...input_manager import InputManager
from .in_game_states.in_game_state_manager import InGameStateManager
from .map import Map


class InGameManager:
    """
    インゲームのマップとステート管理を担当。
    """

    def __init__(self, stage_number: int = 1) -> None:
        self.map = Map(width=16, height=12)
        self.state_manager = InGameStateManager()

    def change_scene(self, scene_name: str) -> None:
        """
        シーン遷移コールバックを呼び出す。
        Args:
            scene_name (str): 遷移先シーン名（例: "title"）
        """
        ...

    def update(self, input_manager: "InputManager") -> None:
        """
        インゲームの状態更新処理。
        """
        self.state_manager.update(self, input_manager)

    def draw(self, game: "Game") -> None:
        """
        インゲームの描画処理。
        """
        self.state_manager.draw(self)
