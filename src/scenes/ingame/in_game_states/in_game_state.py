"""
インゲームの状態管理用Protocol。
各状態（待機・プレイ・クリア・ゲームオーバー等）はこのインターフェースを実装する。
"""

from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from scenes.in_game_scene import InGameScene
    from game import Game
    from input_manager import InputManager
    from .in_game_state_manager import InGameStateManager


class GameStateProtocol(Protocol):
    """
    インゲーム状態のインターフェース。
    各状態はupdate/drawを実装すること。
    """

    def update(self, scene: "InGameStateManager", game: "Game", input_manager: "InputManager") -> None:
        """
        状態ごとの更新処理。

        Args:
            scene (InGameScene): インゲームシーン本体
            game (Game): ゲーム管理クラス
            input_manager (InputManager): 入力管理クラス
        """
        ...

    def draw(self, scene: "InGameScene", game: "Game") -> None:
        """
        状態ごとの描画処理。

        Args:
            scene (InGameScene): インゲームシーン本体
            game (Game): ゲーム管理クラス
        """
        ...
