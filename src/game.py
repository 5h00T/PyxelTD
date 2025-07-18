"""
ゲームループ本体とシーン管理を行うGameクラス。
"""

import pyxel
from scenes import TitleScene
from input_manager import InputManager


class Game:
    """
    ゲーム全体のループとシーン管理を担当するクラス。
    """
    def __init__(self):
        pyxel.init(160, 120)
        self.input_manager = InputManager([
            pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_LEFT, pyxel.KEY_RIGHT,
            pyxel.KEY_SPACE, pyxel.KEY_RETURN, pyxel.KEY_ESCAPE, pyxel.KEY_P, pyxel.KEY_Q
        ])
        self.current_scene = TitleScene()
        pyxel.run(self.update, self.draw)

    def update(self):
        """
        毎フレーム呼び出し。入力更新→現在のシーンの更新処理。
        """
        self.input_manager.update()
        if self.current_scene:
            self.current_scene.update(self, self.input_manager)

    def draw(self):
        """
        現在のシーンの描画処理を呼び出す。
        """
        if self.current_scene:
            self.current_scene.draw(self, self.input_manager)
    
    def change_scene(self, new_scene):
        """
        シーンを変更する。
        
        Args:
            new_scene: 新しいシーンのインスタンス
        """
        self.current_scene = new_scene
