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
from .scene_type import SceneType
from ..utils.font_renderer import FontRenderer


class TitleScene(BaseScene):
    """
    ゲームのタイトル画面を管理するシーン。
    """

    def __init__(self) -> None:
        super().__init__()

    def update(self, game: Game, input_manager: InputManager) -> None:
        """
        タイトル画面の更新処理。
        Zキーでメニューシーンに遷移。
        """
        if input_manager.is_triggered(pyxel.KEY_Z):
            game.change_scene(new_scene=SceneType.MENU)

    def draw(self, game: Game) -> None:
        """
        タイトル画面の描画処理。
        """
        pyxel.cls(0)
        font_renderer = FontRenderer.get_instance()
        font_renderer.draw_text(60, 50, "PyxelTD", 7, font_name="default")
        font_renderer.draw_text(40, 70, "Press Z to start", 6, font_name="default")
