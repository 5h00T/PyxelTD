from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game
    from ..input_manager import InputManager
"""
InGameScene - インゲーム画面のシーン
"""
import pyxel

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

    def __init__(self, stage_number: int = 1) -> None:
        super().__init__()
        self.stage_number = stage_number
        self.manager = InGameManager(self, stage_number)

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
            game.change_scene(new_scene=SceneType.IN_GAME)
        elif result == InGameResult.STAGE_SELECT:
            game.change_scene(new_scene=SceneType.STAGE_SELECT)

    def draw(self, game: "Game") -> None:
        """
        インゲーム画面の描画処理。
        状態管理はmanagerに委譲。
        """
        self.manager.draw(game)

    def is_cleared(self) -> bool:
        """
        ゲームクリア判定。
        クリア条件を満たしたらTrue。
        """
        return False  # TODO: 実装

    def is_gameover(self) -> bool:
        """
        ゲームオーバー判定。
        ゲームオーバー条件を満たしたらTrue。
        """
        return False  # TODO: 実装

    def draw_text_center(self, text: str, y: int = 60, color: int = 7) -> None:
        """
        画面中央にテキストを描画するユーティリティ。
        """
        x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(x, y, text, color)
