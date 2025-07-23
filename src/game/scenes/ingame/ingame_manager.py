from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...game import Game
    from ...input_manager import InputManager
    from ..in_game_scene import InGameScene
from .in_game_states.in_game_state_manager import InGameStateManager
from .map import Map
from .enemy.enemy_manager import EnemyManager
from .ingame_result import InGameResult
from ...utils.font_renderer import FontRenderer


class Unit:
    """Class representing a player-placeable unit."""

    def __init__(self, name: str, icon: int, description: str = "") -> None:
        self.name = name
        self.icon = icon
        self.description = description

    def __repr__(self) -> str:
        return f"Unit(name={self.name}, icon={self.icon})"


"""
InGameManager - インゲームのマップとステート管理を一元化するクラス。
"""


class InGameManager:
    """
    インゲームのマップとステート管理を担当。
    """

    def __init__(self, ingame_scene: "InGameScene", stage_number: int = 1) -> None:
        self.ingame_scene = ingame_scene
        # 仮: ステージごとにサイズ可変、最低14x14保証
        self.stage_number = stage_number
        width = max(16, 14)
        height = max(12, 14)
        self.map = Map(width=width, height=height)
        self.enemy_manager = EnemyManager()
        # --- ステージマスターデータ・マネージャ ---
        from .stage_master import SAMPLE_STAGE_MASTER
        from .stage_manager import StageManager

        # マップ生成後にパスをセット
        SAMPLE_STAGE_MASTER.paths = self.map.get_all_paths_from_entrances_to_goal()
        self.stage_manager = StageManager(SAMPLE_STAGE_MASTER, self.enemy_manager)
        self.state_manager = InGameStateManager(self.enemy_manager)
        from .cursor import Cursor
        from .camera import Camera

        self.cursor = Cursor(self.map.width, self.map.height)
        self.camera = Camera(self.map.width, self.map.height)

        # --- Player unit master ---
        from .player_unit.player_unit import PLAYER_UNIT_MASTER
        from .player_unit.player_unit_manager import PlayerUnitManager

        self.unit_list = PLAYER_UNIT_MASTER
        self.player_unit_manager = PlayerUnitManager()

        # --- Unit list UI state ---
        self.is_selecting_unit: bool = False
        self.selected_cell: Optional[tuple[int, int]] = None
        self.unit_ui_cursor: int = 0

        # --- Base HP ---
        self.base_hp: int = 2  # 防衛拠点のHP
        self.max_base_hp = self.base_hp  # 最大HP

    def update(self, input_manager: "InputManager") -> InGameResult:
        """
        インゲームの状態更新処理。
        現在のステートのupdateのみ呼び出し、
        ゲーム進行・カーソル・カメラ・エネミー等はplaying_stateでのみ動作する。
        """
        state_result = self.state_manager.update(self, input_manager)
        result: InGameResult = InGameResult.NONE
        from .in_game_states.state_result import StateResult

        if state_result == StateResult.RETRY:
            result = InGameResult.RETRY
        elif state_result == StateResult.STAGE_SELECT:
            result = InGameResult.STAGE_SELECT
        return result

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
        # --- ユニット描画 ---
        self.player_unit_manager.draw(camera_x, camera_y)
        self.enemy_manager.draw(camera_x, camera_y)  # エネミーの描画

        # --- マップ描画範囲外を塗りつぶす（右・下のみ） ---
        self.mask_outside_map_area()

        # --- ユニット配置UIの描画 ---
        import pyxel

        if self.is_selecting_unit:
            ui_x = pyxel.width - 60  # 右端から60px幅のUI
            ui_y = 16
            ui_w = 56
            ui_h = 12 + 16 * len(self.unit_list)
            pyxel.rect(ui_x, ui_y, ui_w, ui_h, 5)  # UI背景
            # FontRenderer.draw_text(21, 18, s, 7, font_name="gothic")
            # pyxel.text(ui_x + 4, ui_y + 2, "ユニット選択", 7)
            FontRenderer.draw_text(ui_x + 4, ui_y + 2, "ユニット選択", 7, font_name="default")
            for idx, unit in enumerate(self.unit_list):
                y = ui_y + 16 + idx * 16
                # 選択中はハイライト
                if idx == self.unit_ui_cursor:
                    pyxel.rect(ui_x + 2, y - 2, ui_w - 4, 14, 6)
                # pyxel.text(ui_x + 8, y, f"{unit.name}", 1 if idx == self.unit_ui_cursor else 0)
                FontRenderer.draw_text(
                    ui_x + 8, y + 8, f"{unit.name}", 1 if idx == self.unit_ui_cursor else 0, font_name="default"
                )
            # 選択中ユニットの説明
            sel_unit = self.unit_list[self.unit_ui_cursor]
            # pyxel.text(ui_x + 4, ui_y + ui_h - 12, sel_unit.description, 13)
            FontRenderer.draw_text(ui_x + 4, ui_y + ui_h - 12, sel_unit.description, 13, font_name="default")

        # --- Base HP表示 ---
        # pyxel.text(8, 4, f"BASE HP: {self.base_hp}/{self.max_base_hp}", 6 if self.base_hp <= 3 else 7)
        FontRenderer.draw_text(
            8, 4, f"BASE HP: {self.base_hp}/{self.max_base_hp}", 6 if self.base_hp <= 3 else 7, font_name="default"
        )

        # カーソルは上に描画
        self.cursor.draw(camera_x, camera_y)
        # self.state_manager.draw(self)

    def can_place_unit_at(self, x: int, y: int) -> bool:
        """
        Returns True if a player unit can be placed at (x, y).
        Not placeable if:
        - Already occupied
        - Out of map bounds
        - Not a placeable tile (tile != 1)
        """
        if (x, y) in self.player_unit_manager.units:
            return False
        if not (0 <= x < self.map.width and 0 <= y < self.map.height):
            return False
        tile = self.map.get_tile(x, y)
        if tile != 1:
            return False
        return True

    def mask_outside_map_area(self) -> None:
        """
        マップ描画範囲外（右・下）を黒で塗りつぶす。
        画面左上からマップを描画する前提。
        """
        import pyxel
        from .constants import TILE_SIZE, VIEW_TILE_WIDTH, VIEW_TILE_HEIGHT

        map_screen_w = VIEW_TILE_WIDTH * TILE_SIZE
        map_screen_h = VIEW_TILE_HEIGHT * TILE_SIZE
        mask_color = 0  # 黒で塗りつぶし

        # 右側の余白
        if map_screen_w < pyxel.width:
            pyxel.rect(map_screen_w, 0, pyxel.width - map_screen_w, pyxel.height, mask_color)
        # 下側の余白
        if map_screen_h < pyxel.height:
            pyxel.rect(0, map_screen_h, pyxel.width, pyxel.height - map_screen_h, mask_color)
