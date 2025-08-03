from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game
    from ..input_manager import InputManager
"""
MenuScene - メニュー画面のシーン
"""
import pyxel

from .base_scene import BaseScene
from .scene_type import SceneType
from ..utils.font_renderer import FontRenderer


class MenuScene(BaseScene):
    """
    ゲームのメニュー画面を管理するシーン。
    """

    def __init__(self) -> None:
        super().__init__()
        self.selected_option = 0
        self.options = ["Start Game", "Settings", "Exit"]

    def update(self, game: Game, input_manager: InputManager) -> None:
        """
        メニュー画面の更新処理。
        上下キーで選択、Zで決定。
        InputManager経由で入力判定。
        """
        if input_manager.is_triggered(pyxel.KEY_UP):
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif input_manager.is_triggered(pyxel.KEY_DOWN):
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif input_manager.is_triggered(pyxel.KEY_Z):
            if self.selected_option == 0:  # Start Game
                game.change_scene(new_scene=SceneType.STAGE_SELECT)
            elif self.selected_option == 1:  # Settings
                # TODO: Implement settings scene
                pass
            elif self.selected_option == 2:  # Exit
                pyxel.quit()

    def draw(self, game: Game) -> None:
        """
        メニュー画面の描画処理。
        """
        pyxel.cls(0)
        font_renderer = FontRenderer.get_instance()
        font_renderer.draw_text(70, 30, "MENU", 7, font_name="default")
        for i, option in enumerate(self.options):
            color = 11 if i == self.selected_option else 6
            y_pos = 50 + i * 15
            font_renderer.draw_text(60, y_pos, option, color, font_name="default")
        font_renderer.draw_text(30, 100, "UP/DOWN:カーソル移動, Z:決定", 5, font_name="default")
