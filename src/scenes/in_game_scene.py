"""
InGameScene - インゲーム画面のシーン
"""
import pyxel
from .base_scene import BaseScene


class InGameScene(BaseScene):
    """
    ゲームプレイ中の画面を管理するシーン。
    """
    
    def __init__(self, stage_number=1):
        super().__init__()
        self.stage_number = stage_number
        self.game_state = "playing"  # playing, paused, game_over
    
    def update(self, game):
        """
        インゲーム画面の更新処理。
        ESCでポーズ/メニューに戻る、今後ゲームロジックを追加。
        """
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            if self.game_state == "playing":
                self.game_state = "paused"
            else:
                from .menu_scene import MenuScene
                game.change_scene(MenuScene())
        elif pyxel.btnp(pyxel.KEY_SPACE) and self.game_state == "paused":
            self.game_state = "playing"
        
        # TODO: ゲームロジックの実装
        # - 敵の管理
        # - タワーの配置
        # - 弾の軌道
        # - スコア計算
        # など
    
    def draw(self, game):
        """
        インゲーム画面の描画処理。
        """
        pyxel.cls(3)  # 緑背景でゲーム画面を表現
        
        # ステージ情報表示
        pyxel.text(5, 5, f"Stage {self.stage_number}", 7)
        
        if self.game_state == "playing":
            # TODO: ゲーム要素の描画
            # - マップ
            # - タワー
            # - 敵
            # - UI
            pyxel.text(60, 50, "Game Playing", 7)
            pyxel.text(40, 60, "(Game logic here)", 6)
            pyxel.text(40, 110, "ESC: Pause", 5)
        elif self.game_state == "paused":
            # ポーズ画面
            pyxel.rect(40, 40, 80, 40, 0)
            pyxel.rectb(40, 40, 80, 40, 7)
            pyxel.text(65, 50, "PAUSED", 7)
            pyxel.text(45, 60, "SPACE: Resume", 6)
            pyxel.text(50, 70, "ESC: Menu", 6)