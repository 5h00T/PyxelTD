"""
ゲームループ本体とシーン管理を行うGameクラス。
"""
import pyxel

class Game:
    """
    ゲーム全体のループとシーン管理を担当するクラス。
    """
    def __init__(self):
        pyxel.init(160, 120)
        # 今後: self.scene = TitleScene() などでシーン管理
        pyxel.run(self.update, self.draw)

    def update(self):
        # 今後: self.scene.update(self) などでシーンごとに処理を分岐
        pass

    def draw(self):
        pyxel.cls(0)
        # 今後: self.scene.draw(self) などでシーンごとに描画を分岐
