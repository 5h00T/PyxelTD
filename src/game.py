"""
ゲームループ本体とシーン管理を行うGameクラス。
"""
import pyxel
from scenes import TitleScene


class Game:
    """
    ゲーム全体のループとシーン管理を担当するクラス。
    """
    def __init__(self):
        pyxel.init(160, 120)
        self.current_scene = TitleScene()
        pyxel.run(self.update, self.draw)

    def update(self):
        """現在のシーンの更新処理を呼び出す"""
        if self.current_scene:
            self.current_scene.update(self)

    def draw(self):
        """現在のシーンの描画処理を呼び出す"""
        if self.current_scene:
            self.current_scene.draw(self)
    
    def change_scene(self, new_scene):
        """
        シーンを変更する。
        
        Args:
            new_scene: 新しいシーンのインスタンス
        """
        self.current_scene = new_scene
