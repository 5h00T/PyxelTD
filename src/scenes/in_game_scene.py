"""
InGameScene - インゲーム画面のシーン
"""
import pyxel
from .base_scene import BaseScene
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game
    from input_manager import InputManager


class InGameScene(BaseScene):
    """
    ゲームプレイ中の画面を管理するシーン。
    """
    
    def __init__(self, stage_number: int = 1) -> None:
        super().__init__()
        self.stage_number = stage_number
        self.game_state = "playing"  # playing, paused, game_over

    def update(self, game: "Game", input_manager: "InputManager") -> None:
        """
        インゲーム画面の更新処理。
        Pでポーズ、Qでメニューに戻る、今後ゲームロジックを追加。
        InputManager経由で入力判定。
        """
        if input_manager.is_triggered(pyxel.KEY_P):
            if self.game_state == "playing":
                self.game_state = "paused"
            elif self.game_state == "paused":
                self.game_state = "playing"
        elif input_manager.is_triggered(pyxel.KEY_Q):
            from .menu_scene import MenuScene
            game.change_scene(MenuScene())
        
        # TODO: ゲームロジックの実装
        # - 敵の管理
        # - タワーの配置
        # - 弾の軌道
        # - スコア計算
        # など
    
    def draw(self, game: "Game", input_manager: "InputManager") -> None:
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
            pyxel.text(40, 110, "P: Pause, Q: Menu", 5)
        elif self.game_state == "paused":
            # ポーズ画面
            pyxel.rect(40, 40, 80, 40, 0)
            pyxel.rectb(40, 40, 80, 40, 7)
            pyxel.text(65, 50, "PAUSED", 7)
            pyxel.text(50, 60, "P: Resume", 6)
            pyxel.text(55, 70, "Q: Menu", 6)