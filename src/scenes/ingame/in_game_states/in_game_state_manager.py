"""
InGameStateManager - インゲームのステート管理クラス。
各状態インスタンスの生成・保持・遷移を一元管理。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scenes.in_game_scene import InGameScene
    from game import Game
    from input_manager import InputManager
from .prestart_state import PreStartState
from .playing_state import PlayingState
from .clear_state import ClearState
from .gameover_state import GameOverState
from .in_game_state import GameStateProtocol


class InGameStateManager:
    """
    インゲームのステート管理クラス。
    状態インスタンスの生成・保持・遷移を担当。
    """

    def __init__(self) -> None:
        self.prestart_state = PreStartState()
        self.playing_state = PlayingState()
        self.clear_state = ClearState()
        self.gameover_state = GameOverState()
        self.current_state: GameStateProtocol = self.prestart_state

    def change_state(self, new_state: GameStateProtocol) -> None:
        """
        状態を変更する。
        Args:
            new_state (GameStateProtocol): 新しい状態インスタンス
        """
        print(f"Changing state to {new_state.__class__.__name__}")
        self.current_state = new_state

    def update(self, scene: "InGameScene", game: "Game", input_manager: "InputManager") -> None:
        """
        現在の状態の更新処理。
        """
        self.current_state.update(self, game, input_manager)

    def draw(self, scene: "InGameScene", game: "Game") -> None:
        """
        現在の状態の描画処理。
        """
        self.current_state.draw(scene, game)
