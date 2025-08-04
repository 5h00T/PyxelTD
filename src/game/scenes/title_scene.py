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
        title_text = "PyxelTD"
        width = font_renderer.text_width(title_text, font_name="default")
        text_x = (game.WINDOW_WIDTH - width) // 2
        font_renderer.draw_text(text_x, 50, title_text, 7, font_name="default")
        description_text = "Press Z to start"
        desc_width = font_renderer.text_width(description_text, font_name="default")
        desc_x = (game.WINDOW_WIDTH - desc_width) // 2
        font_renderer.draw_text(desc_x, 70, description_text, 6, font_name="default")
