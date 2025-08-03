"""
インゲームの状態管理用Protocol。
各状態（待機・プレイ・クリア・ゲームオーバー等）はこのインターフェースを実装する。
"""

from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager

from .state_result import StateResult


class GameStateProtocol(Protocol):
    """
    インゲーム状態のインターフェース。
    各状態はupdate/drawを実装すること。
    """

    def setup(self) -> None:
        """
        状態の初期化処理。
        必要に応じて実装する。
        """
        pass

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> StateResult:
        """
        状態ごとの更新処理。

        Args:
            scene (InGameScene): インゲームシーン本体
            game (Game): ゲーム管理クラス
            input_manager (InputManager): 入力管理クラス
        """
        ...

    def draw(self, manager: "InGameManager") -> None:
        """
        状態ごとの描画処理。

        Args:
            scene (InGameScene): インゲームシーン本体
            game (Game): ゲーム管理クラス
        """
        ...
