"""
TitleScene - タイトル画面のシーン
"""
import pyxel
from .base_scene import BaseScene


class TitleScene(BaseScene):
    """
    ゲームのタイトル画面を管理するシーン。
    """
    
    def __init__(self):
        super().__init__()
    
    def update(self, game):
        """
        タイトル画面の更新処理。
        スペースキーでメニューシーンに遷移。
        """
        if pyxel.btnp(pyxel.KEY_SPACE):
            from .menu_scene import MenuScene
            game.change_scene(MenuScene())
    
    def draw(self, game):
        """
        タイトル画面の描画処理。
        """
        pyxel.cls(0)
        pyxel.text(60, 50, "PyxelTD", 7)
        pyxel.text(40, 70, "Press SPACE to start", 6)