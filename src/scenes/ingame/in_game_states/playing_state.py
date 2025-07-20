"""
ゲームプレイ中のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scenes.in_game_scene import InGameScene
    from game import Game
    from input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
from .in_game_state import GameStateProtocol


class PlayingState(GameStateProtocol):
    """
    ゲームプレイ中の状態。
    クリア・ゲームオーバー判定で状態遷移。
    """

    def update(self, state_manager: "InGameStateManager", game: "Game", input_manager: "InputManager") -> None:
        # TODO: ゲームロジック更新
        ...

    def draw(self, scene: "InGameScene", game: "Game") -> None:
        # ゲームプレイ画面描画
        scene.draw_gameplay()
