from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game
    from ..input_manager import InputManager
"""
TitleScene - タイトル画面のシーン
"""
import pyxel
from .base_scene import BaseScene


class TitleScene(BaseScene):
    """
    ゲームのタイトル画面を管理するシーン。
    """

    def __init__(self) -> None:
        super().__init__()

    def update(self, game: Game, input_manager: InputManager) -> None:
        """
        タイトル画面の更新処理。
        スペースキーでメニューシーンに遷移。
        """
        if input_manager.is_triggered(pyxel.KEY_SPACE):
            from ..game import SceneType  # 遅延インポートで循環参照回避

            game.change_scene(new_scene=SceneType.MENU)

    def draw(self, game: Game) -> None:
        """
        タイトル画面の描画処理。
        """
        pyxel.cls(0)
        pyxel.text(60, 50, "PyxelTD", 7)
        pyxel.text(40, 70, "Press SPACE to start", 6)
