"""
ゲームプレイ中のステートクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....input_manager import InputManager
    from .in_game_state_manager import InGameStateManager
    from ..ingame_manager import InGameManager
from .in_game_state import GameStateProtocol
from ..enemy.enemy_manager import EnemyManager
from .state_result import StateResult
from ..enemy.enemy import Enemy


class PlayingState(GameStateProtocol):
    """
    ゲームプレイ中の状態。
    クリア・ゲームオーバー判定で状態遷移。
    """

    def __init__(self, enemy_manager: "EnemyManager") -> None:
        """
        初期化処理。
        必要な変数や状態を設定。
        """
        self.enemy_manager = enemy_manager

    def update(
        self, state_manager: "InGameStateManager", manager: "InGameManager", input_manager: "InputManager"
    ) -> StateResult:
        """
        ゲームプレイ中の状態更新処理。
        各役割ごとに分割したメソッドを呼び出し、主処理はフロー制御のみとする。
        """
        self._update_stage_and_units(manager)
        self._update_enemies(manager, state_manager)
        if manager.is_selecting_unit:
            return self._handle_unit_selection_ui(manager, input_manager)
        self._handle_normal_input(manager, input_manager)
        self._update_camera(manager)
        return StateResult.NONE

    def _update_stage_and_units(self, manager: "InGameManager") -> None:
        """
        ステージ進行・プレイヤーユニットの更新を行う。
        """
        manager.stage_manager.update()
        manager.player_unit_manager.update(manager.enemy_manager)

    def _update_enemies(self, manager: "InGameManager", state_manager: "InGameStateManager") -> list[Enemy]:
        """
        エネミーの更新とゴール・ゲームオーバー判定を行う。
        Returns:
            list: ゴール到達したエネミーリスト
        """
        goal_enemies = self.enemy_manager.update()
        if goal_enemies:
            print(f"Goal reached by {len(goal_enemies)} enemies!")
            manager.base_hp -= len(goal_enemies)
            # ゴール到達エネミーはリストから除去
            self.enemy_manager.enemies = [e for e in self.enemy_manager.enemies if not (e.is_goal() and e.is_alive)]
            if manager.base_hp <= 0:
                # ゲームオーバー遷移
                state_manager.change_state(state_manager.gameover_state)
        return goal_enemies

    def _handle_unit_selection_ui(self, manager: "InGameManager", input_manager: "InputManager") -> StateResult:
        """
        ユニット選択UIの操作を処理する。
        ユニット選択中はカーソル・Zキー操作を無効化。
        """
        import pyxel

        if input_manager.is_triggered(pyxel.KEY_UP):
            manager.unit_ui_cursor = (manager.unit_ui_cursor - 1) % len(manager.unit_list)
        elif input_manager.is_triggered(pyxel.KEY_DOWN):
            manager.unit_ui_cursor = (manager.unit_ui_cursor + 1) % len(manager.unit_list)
        elif input_manager.is_triggered(pyxel.KEY_Z):
            if manager.selected_cell is not None:
                x, y = manager.selected_cell
                unit = manager.unit_list[manager.unit_ui_cursor]
                manager.player_unit_manager.place_unit(unit, x, y)
            manager.is_selecting_unit = False
            manager.selected_cell = None
        elif input_manager.is_triggered(pyxel.KEY_X):
            manager.is_selecting_unit = False
            manager.selected_cell = None
        return StateResult.NONE

    def _handle_normal_input(self, manager: "InGameManager", input_manager: "InputManager") -> None:
        """
        通常時のカーソル移動・Zキーによるユニット配置モード遷移を処理する。
        """
        import pyxel

        if input_manager.is_triggered(pyxel.KEY_UP):
            manager.cursor.move(0, -1)
        elif input_manager.is_triggered(pyxel.KEY_DOWN):
            manager.cursor.move(0, 1)
        elif input_manager.is_triggered(pyxel.KEY_LEFT):
            manager.cursor.move(-1, 0)
        elif input_manager.is_triggered(pyxel.KEY_RIGHT):
            manager.cursor.move(1, 0)

        # Zキーでユニット配置モードへ
        if input_manager.is_triggered(pyxel.KEY_Z):
            x, y = manager.cursor.get_pos()
            if manager.can_place_unit_at(x, y):
                manager.is_selecting_unit = True
                manager.selected_cell = (x, y)
                manager.unit_ui_cursor = 0

    def _update_camera(self, manager: "InGameManager") -> None:
        """
        カメラの追従処理。
        """
        manager.camera.move_to_cursor(*manager.cursor.get_pos())

    def draw(self, manager: "InGameManager") -> None:
        """
        マップの描写を行う。
        """
        # manager.map.draw()
