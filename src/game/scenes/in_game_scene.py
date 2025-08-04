from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..game import Game
    from ..input_manager import InputManager
"""
InGameScene - インゲーム画面のシーン
"""
from .base_scene import BaseScene
from .ingame.in_game_states.in_game_state import GameStateProtocol
from .ingame.ingame_manager import InGameManager
from .scene_type import SceneType
from .ingame.ingame_result import InGameResult


class InGameScene(BaseScene):
    """
    ゲームプレイ中の画面を管理するシーン。
    ステートパターンで状態管理。
    """

    def __init__(self, scene_param: dict[str, Any] | None = None) -> None:
        super().__init__()
        stage_index = 0
        if scene_param is not None and "stage_index" in scene_param:
            stage_index = scene_param["stage_index"]
        self.stage_index = stage_index
        self.manager = InGameManager(self, stage_index)

    def change_state(self, new_state: GameStateProtocol) -> None:
        """
        インゲームの状態を変更する。
        Args:
            new_state (GameStateProtocol): 新しい状態インスタンス
        """
        self.manager.state_manager.change_state(new_state)

    def update(self, game: "Game", input_manager: "InputManager") -> None:
        """
        インゲーム画面の更新処理。
        状態管理はmanagerに委譲。
        """
        result = self.manager.update(input_manager)
        if result == InGameResult.RETRY:
            game.change_scene(new_scene=SceneType.IN_GAME, scene_param={"stage_index": self.stage_index})
        elif result == InGameResult.STAGE_SELECT:
            game.change_scene(new_scene=SceneType.STAGE_SELECT)

    def draw(self, game: "Game") -> None:
        """
        インゲーム画面の描画処理。
        状態管理はmanagerに委譲。
        """
        self.manager.draw(game)
