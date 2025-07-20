from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game
    from ..input_manager import InputManager
"""
StageSelectScene - ステージ選択画面のシーン
"""
import pyxel

from .base_scene import BaseScene
from .scene_type import SceneType


class StageSelectScene(BaseScene):
    """
    ステージ選択画面を管理するシーン。
    """

    def __init__(self) -> None:
        super().__init__()
        self.selected_stage = 0
        self.stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4"]

    def update(self, game: Game, input_manager: InputManager) -> None:
        """
        ステージ選択画面の更新処理。
        上下キーで選択、スペースキーで決定、Qでメニューに戻る。
        InputManager経由で入力判定。
        """
        if input_manager.is_triggered(pyxel.KEY_UP):
            self.selected_stage = (self.selected_stage - 1) % len(self.stages)
        elif input_manager.is_triggered(pyxel.KEY_DOWN):
            self.selected_stage = (self.selected_stage + 1) % len(self.stages)
        elif input_manager.is_triggered(pyxel.KEY_SPACE):
            game.change_scene(new_scene=SceneType.IN_GAME)
        elif input_manager.is_triggered(pyxel.KEY_Q):
            game.change_scene(new_scene=SceneType.MENU)

    def draw(self, game: Game) -> None:
        """
        ステージ選択画面の描画処理。
        """
        pyxel.cls(0)
        pyxel.text(55, 20, "SELECT STAGE", 7)

        for i, stage in enumerate(self.stages):
            color = 11 if i == self.selected_stage else 6
            y_pos = 40 + i * 15
            pyxel.text(60, y_pos, stage, color)

        pyxel.text(20, 100, "UP/DOWN: Select, SPACE: Start", 5)
        pyxel.text(25, 110, "Q: Back to Menu", 5)
