"""
InGameManager - インゲームのマップとステート管理を一元化するクラス。
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...game import Game
    from ...input_manager import InputManager
from .in_game_states.in_game_state_manager import InGameStateManager
from .map import Map
from .enemy_manager import EnemyManager


class InGameManager:
    """
    インゲームのマップとステート管理を担当。
    """

    def __init__(self, stage_number: int = 1) -> None:
        # 仮: ステージごとにサイズ可変、最低14x14保証
        width = max(16, 14)
        height = max(12, 14)
        self.map = Map(width=width, height=height)
        self.enemy_manager = EnemyManager()
        # エネミーのサンプル生成（マップ経路に沿う）
        self.enemy_manager.spawn_sample_enemies(self.map)
        self.state_manager = InGameStateManager(self.enemy_manager)
        from .cursor import Cursor
        from .camera import Camera

        self.cursor = Cursor(self.map.width, self.map.height)
        self.camera = Camera(self.map.width, self.map.height)

    def change_scene(self, scene_name: str) -> None:
        """
        シーン遷移コールバックを呼び出す。
        Args:
            scene_name (str): 遷移先シーン名（例: "title"）
        """
        ...

    def update(self, input_manager: "InputManager") -> None:
        """
        インゲームの状態更新処理。
        カーソル・カメラの移動も管理。
        """
        # カーソル移動（仮: 矢印キーで移動）
        import pyxel

        if input_manager.is_triggered(pyxel.KEY_UP):
            self.cursor.move(0, -1)
        elif input_manager.is_triggered(pyxel.KEY_DOWN):
            self.cursor.move(0, 1)
        elif input_manager.is_triggered(pyxel.KEY_LEFT):
            self.cursor.move(-1, 0)
        elif input_manager.is_triggered(pyxel.KEY_RIGHT):
            self.cursor.move(1, 0)
        # カメラ移動
        self.camera.move_to_cursor(*self.cursor.get_pos())
        self.state_manager.update(self, input_manager)

    def draw(self, game: "Game") -> None:
        """
        インゲームの描画処理。
        カメラ・カーソルを考慮して描画。
        """

        # TODO: ゲーム画面の背景表示
        def draw_background() -> None:
            import pyxel

            pyxel.cls(0)

        draw_background()

        camera_x, camera_y = self.camera.get_pos()
        # マップ描画（カメラ範囲のみ）
        self.map.draw(camera_x, camera_y, self.camera.view_width, self.camera.view_height)
        # TODO: ユニットなどの描画
        self.enemy_manager.draw(camera_x, camera_y)  # エネミーの描画
        # カーソルは上に描画
        self.cursor.draw(camera_x, camera_y)
        # self.state_manager.draw(self)
