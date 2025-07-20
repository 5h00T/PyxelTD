from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
    from input_manager import InputManager
"""
InGameScene - インゲーム画面のシーン
"""
import pyxel
from .base_scene import BaseScene
from .ingame.in_game_states.in_game_state import GameStateProtocol


class InGameScene(BaseScene):
    """
    ゲームプレイ中の画面を管理するシーン。
    ステートパターンで状態管理。
    """

    def __init__(self, stage_number: int = 1) -> None:
        super().__init__()
        self.stage_number = stage_number
        from .ingame.in_game_states.in_game_state_manager import InGameStateManager

        self.state_manager = InGameStateManager()

    def change_state(self, new_state: GameStateProtocol) -> None:
        """
        インゲームの状態を変更する。
        Args:
            new_state (GameStateProtocol): 新しい状態インスタンス
        """
        self.state_manager.change_state(new_state)

    def update(self, game: "Game", input_manager: "InputManager") -> None:
        """
        インゲーム画面の更新処理。
        状態管理はstate_managerに委譲。
        """
        self.state_manager.update(self, game, input_manager)

    def draw(self, game: "Game") -> None:
        """
        インゲーム画面の描画処理。
        状態管理はstate_managerに委譲。
        """
        self.state_manager.draw(self, game)

    def draw_gameplay(self) -> None:
        """
        ゲームプレイ中の描画処理。
        ここにマップ・敵・タワー・UI等の描画処理を記述。
        """
        pyxel.cls(3)
        pyxel.text(5, 5, f"Stage {self.stage_number}", 7)
        pyxel.text(60, 50, "Game Playing", 7)
        pyxel.text(40, 60, "(Game logic here)", 6)
        pyxel.text(40, 110, "P: Pause, Q: Menu", 5)

    def is_cleared(self) -> bool:
        """
        ゲームクリア判定。
        クリア条件を満たしたらTrue。
        """
        return False  # TODO: 実装

    def is_gameover(self) -> bool:
        """
        ゲームオーバー判定。
        ゲームオーバー条件を満たしたらTrue。
        """
        return False  # TODO: 実装

    def draw_text_center(self, text: str, y: int = 60, color: int = 7) -> None:
        """
        画面中央にテキストを描画するユーティリティ。
        """
        x = (pyxel.width - len(text) * 4) // 2
        pyxel.text(x, y, text, color)
