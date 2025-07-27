"""
ゲーム開始前（待機状態）のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol
from .state_result import StateResult
from ....utils.font_renderer import FontRenderer


class PreStartState(GameStateProtocol):
    """
    ゲーム開始前の待機状態。
    スタート入力でPlayingStateへ遷移。
    """

    def setup(self) -> None:
        """
        状態の初期化処理。
        アニメーション用のカウンタと状態を初期化。
        """
        self.frame_count = 0
        self.anim_state = "enter"  # enter:上から下, wait:中央停止, exit:下に流れる
        self.text_init_y = -16  # テキストの初期Y座標（画面外上）
        self.text_y = self.text_init_y  # テキストの初期Y座標（画面外上）
        self.text_end_y = 136  # テキストの終了Y座標（画面外下）
        self.text_x = 60
        self.text_target_y = (self.text_end_y - self.text_init_y) / 2 + self.text_init_y  # 画面中央Y
        self.enter_speed = 4  # 上から中央までの速度
        self.exit_speed = 4  # 下への速度
        self.wait_frames = 30  # 中央で停止するフレーム数
        self._wait_counter = 0

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> StateResult:
        """
        アニメーション状態に応じてテキストのY座標を更新。
        スペースキーでゲーム開始。
        """

        self.frame_count += 1

        # アニメーション制御
        if self.anim_state == "enter":
            # 上から中央へ移動
            self.text_y += self.enter_speed
            if self.text_y >= self.text_target_y:
                self.text_y = self.text_target_y
                self.anim_state = "wait"
        elif self.anim_state == "wait":
            # 中央で一定時間待機
            self._wait_counter += 1
            if self._wait_counter >= self.wait_frames:
                self.anim_state = "exit"
                self._wait_counter = 0
        elif self.anim_state == "exit":
            # 下に流れる
            self.text_y += self.exit_speed
            if self.text_y >= self.text_end_y:
                self.text_y = self.text_end_y
                state_manager.change_state(state_manager.playing_state)

        return StateResult.NONE

    def draw(self, manager: "InGameManager") -> None:
        """
        GAME STARTテキストをアニメーションで描画。
        上から下に流れ、中央で停止し、下に流れて消える。
        """
        FontRenderer.draw_text(self.text_x, int(self.text_y), "GAME START", 15, font_name="default")
