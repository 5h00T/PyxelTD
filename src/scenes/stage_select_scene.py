from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
    from input_manager import InputManager
"""
StageSelectScene - ステージ選択画面のシーン
"""
import pyxel
from .base_scene import BaseScene


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
        上下キーで選択、スペースキーで決定、ESCでメニューに戻る。
        InputManager経由で入力判定。
        """
        if input_manager.is_triggered(pyxel.KEY_UP):
            self.selected_stage = (self.selected_stage - 1) % len(self.stages)
        elif input_manager.is_triggered(pyxel.KEY_DOWN):
            self.selected_stage = (self.selected_stage + 1) % len(self.stages)
        elif input_manager.is_triggered(pyxel.KEY_SPACE):
            from .in_game_scene import InGameScene

            game.change_scene(InGameScene(self.selected_stage + 1))
        elif input_manager.is_triggered(pyxel.KEY_ESCAPE):
            from .menu_scene import MenuScene

            game.change_scene(MenuScene())

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
        pyxel.text(25, 110, "ESC: Back to Menu", 5)
