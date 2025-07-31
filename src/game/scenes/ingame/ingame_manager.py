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
from .constants import TILE_SIZE
from .player_unit.player_unit_manager import PlayerUnitManager


class Unit:
    """
    Class representing a player-placeable unit.
    Attributes:
        name (str): ユニット名
        icon (int): アイコンID
        cost (int): 配置コスト
        description (str): ユニット説明
    """

    def __init__(self, name: str, icon: int, cost: int, description: str = "") -> None:
        self.name = name
        self.icon = icon
        self.cost = cost
        self.description = description

    def __repr__(self) -> str:
        return f"Unit(name={self.name}, icon={self.icon}, cost={self.cost})"


"""
InGameManager - インゲームのマップとステート管理を一元化するクラス。
"""


class InGameManager:
    """
    インゲームのマップとステート管理を担当。
    """

    def __init__(self, ingame_scene: "InGameScene", stage_index: int = 0) -> None:
        self.ingame_scene = ingame_scene
        self.stage_index = stage_index
        from .stage_master import STAGE_MASTER_LIST
        from .stage_manager import StageManager

        stage_data = STAGE_MASTER_LIST[stage_index]
        self.map = Map(map_data=stage_data.map_data)
        self.enemy_manager = EnemyManager()
        # --- ステージマスターデータ・マネージャ ---
        self.stage_manager = StageManager(stage_data, self.enemy_manager, self.map)
        self.state_manager = InGameStateManager(self.enemy_manager)
        from .cursor import Cursor
        from .camera import Camera

        goal_pos = self.map.get_goal()
        self.cursor = Cursor(goal_pos, self.map.width, self.map.height)
        init_pos = goal_pos
        self.camera = Camera(init_pos, self.map.width, self.map.height)

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

        # --- 所持資金 ---
        self.funds: int = 100  # 初期資金

        self.outside_area_color: int = 0  # マップ外の塗りつぶし色

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
        self.draw_background()
        camera_x, camera_y = self.camera.get_pos()
        self.draw_map_and_objects(camera_x, camera_y)
        self.mask_outside_map_area()
        self.draw_range_ring(camera_x, camera_y)
        self.draw_right_ui(game, camera_x, camera_y)
        self.draw_bottom_ui(game)
        self.draw_cursor(camera_x, camera_y)
        self.state_manager.draw(self)

    def draw_background(self) -> None:
        import pyxel

        pyxel.cls(0)

    def draw_map_and_objects(self, camera_x: int, camera_y: int) -> None:
        self.map.draw(camera_x, camera_y, self.camera.view_width, self.camera.view_height)
        self.player_unit_manager.draw(camera_x, camera_y)
        self.enemy_manager.draw(camera_x, camera_y)

    def draw_range_ring(self, camera_x: int, camera_y: int) -> None:
        import pyxel

        pum = self.player_unit_manager
        if pum.is_upgrading_unit and pum.selected_unit_pos is not None:
            x, y = pum.selected_unit_pos
            inst = pum.units[(x, y)]
            unit = inst.unit
            level = inst.level
            next_level = min(level + 1, unit.max_level)
            cx = (x - camera_x) * TILE_SIZE + TILE_SIZE // 2
            cy = (y - camera_y) * TILE_SIZE + TILE_SIZE // 2
            rng = unit.get_range(next_level)
            radius = int(rng * TILE_SIZE)
            pyxel.circb(cx, cy, radius, 13)
        elif not self.is_selecting_unit:
            cursor_pos = self.cursor.get_pos()
            unit_inst = self.player_unit_manager.units.get(cursor_pos)
            if unit_inst is not None:
                rng = unit_inst.unit.get_range(unit_inst.level)
                cx = (cursor_pos[0] - camera_x) * TILE_SIZE + TILE_SIZE // 2
                cy = (cursor_pos[1] - camera_y) * TILE_SIZE + TILE_SIZE // 2
                radius = int(rng * TILE_SIZE)
                pyxel.circb(cx, cy, radius, 10)

    def draw_right_ui(self, game: "Game", camera_x: int, camera_y: int) -> None:
        pum = self.player_unit_manager
        if pum.is_upgrading_unit and pum.selected_unit_pos is not None:
            self._draw_upgrade_ui(game, pum)
        elif self.is_selecting_unit:
            self._draw_unit_select_ui(game)
        else:
            self._draw_default_right_ui(game)

    def _draw_upgrade_ui(self, game: "Game", pum: "PlayerUnitManager") -> None:
        import pyxel

        ui_x = self.camera.view_width * TILE_SIZE
        ui_y = 0
        ui_w = game.WINDOW_WIDTH - ui_x
        ui_h = game.WINDOW_HEIGHT
        pyxel.rect(ui_x, ui_y, ui_w, ui_h, 1)
        title_text = "ユニット強化"
        title_w = len(title_text) * 8
        title_x = ui_x + (ui_w - title_w) // 2
        FontRenderer.draw_text(title_x, ui_y + 4, title_text, 7, font_name="default")
        opt_y = ui_y + 16

        # 強化コスト・資金チェック
        if pum.selected_unit_pos is None:
            x, y = (-1, -1)
        else:
            x, y = pum.selected_unit_pos
        inst = pum.units[(x, y)]
        unit = inst.unit
        level = inst.level
        next_cost = unit.get_upgrade_cost(level)
        can_upgrade = (next_cost > 0) and (self.funds >= next_cost) and (level < unit.max_level)

        # 強化ボタン色: 押せる=10, 押せない=5
        upgrade_color = 10 if can_upgrade and pum.upgrade_ui_cursor == 0 else (7 if can_upgrade else 5)
        FontRenderer.draw_text(ui_x + 4, opt_y, "強化", upgrade_color, font_name="default")
        # コスト表示
        if level < unit.max_level:
            cost_str = f"コスト:{next_cost}"
            cost_color = 3 if can_upgrade else 8
            FontRenderer.draw_text(ui_x + 4, opt_y + 14, cost_str, cost_color, font_name="default")
        else:
            FontRenderer.draw_text(ui_x + 4, opt_y + 14, "最大レベル", 8, font_name="default")

        # キャンセルボタン
        FontRenderer.draw_text(
            ui_x + 4, opt_y + 24, "キャンセル", 10 if pum.upgrade_ui_cursor == 1 else 7, font_name="default"
        )

        FontRenderer.draw_text(ui_x + 8, opt_y + 36, f"Lv: {level}", 7, font_name="default")
        FontRenderer.draw_text(ui_x + 8, opt_y + 46, f"攻撃: {unit.get_attack(level)}", 7, font_name="default")
        FontRenderer.draw_text(ui_x + 8, opt_y + 56, f"射程: {unit.get_range(level)}", 7, font_name="default")
        if level < unit.max_level:
            FontRenderer.draw_text(ui_x + 8, opt_y + 70, f"→ Lv: {level+1}", 13, font_name="default")
            FontRenderer.draw_text(ui_x + 8, opt_y + 80, f"攻:{unit.get_attack(level+1)}", 13, font_name="default")
            FontRenderer.draw_text(ui_x + 8, opt_y + 90, f"射:{unit.get_range(level+1)}", 13, font_name="default")

    def _draw_unit_select_ui(self, game: "Game") -> None:
        import pyxel

        ui_x = self.camera.view_width * TILE_SIZE
        ui_y = 0
        ui_w = game.WINDOW_WIDTH - ui_x
        ui_h = game.WINDOW_HEIGHT
        pyxel.rect(ui_x, ui_y, ui_w, ui_h, 5)
        title_text = "ユニット選択"
        title_w = len(title_text) * 8
        title_x = ui_x + (ui_w - title_w) // 2
        FontRenderer.draw_text(title_x, ui_y + 4, title_text, 7, font_name="default")
        font_h = 8
        item_pad = 4
        item_h = font_h * 2 + item_pad
        list_top = ui_y + 16
        for idx, unit in enumerate(self.unit_list):
            y = list_top + idx * item_h
            can_afford = self.funds >= unit.cost
            if can_afford:
                name_color = 1 if idx == self.unit_ui_cursor else 0
                cost_color = 3
                bg_color = 6 if idx == self.unit_ui_cursor else 5
            else:
                name_color = 1
                cost_color = 3
                bg_color = 13 if idx == self.unit_ui_cursor else 5
            if idx == self.unit_ui_cursor:
                pyxel.rect(ui_x + 2, y - 2, ui_w - 4, item_h, bg_color)
            FontRenderer.draw_text(ui_x + 4, y + 2, f"{unit.name}", name_color, font_name="default")
            cost_str = f"コスト:{unit.cost}"
            FontRenderer.draw_text(ui_x + 4, y + 2 + font_h, cost_str, cost_color, font_name="default")
        sel_unit = self.unit_list[self.unit_ui_cursor]
        desc_y = ui_y + ui_h - 24
        max_desc_width = ui_w - 8
        max_chars_per_line = max_desc_width // 8
        desc_lines = []
        desc = sel_unit.description
        while desc:
            desc_lines.append(desc[:max_chars_per_line])
            desc = desc[max_chars_per_line:]
        for i, line in enumerate(desc_lines[:2]):
            FontRenderer.draw_text(ui_x + 4, desc_y + i * 9, line, 13, font_name="default")

    def _draw_default_right_ui(self, game: "Game") -> None:
        import pyxel

        ui_x = self.camera.view_width * TILE_SIZE
        ui_y = 0
        ui_w = game.WINDOW_WIDTH - ui_x
        ui_h = game.WINDOW_HEIGHT
        pyxel.rect(ui_x, ui_y, ui_w, ui_h, 13)

    def draw_bottom_ui(self, game: "Game") -> None:
        import pyxel

        map_bottom_y = self.camera.view_height * TILE_SIZE
        ui_x = 0
        ui_y = map_bottom_y
        ui_w = self.camera.view_width * TILE_SIZE
        ui_h = game.WINDOW_HEIGHT - map_bottom_y
        pyxel.rect(ui_x, ui_y, ui_w, ui_h, 13)
        funds = self.funds
        funds_text = f"資金: {funds}"
        FontRenderer.draw_text(ui_x + 8, ui_y + 0, funds_text, 1, font_name="default")
        FontRenderer.draw_text(
            8, 4, f"BASE HP: {self.base_hp}/{self.max_base_hp}", 6 if self.base_hp <= 3 else 7, font_name="default"
        )

    def draw_cursor(self, camera_x: int, camera_y: int) -> None:
        self.cursor.draw(camera_x, camera_y)

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

        # 右側の余白
        if map_screen_w < pyxel.width:
            pyxel.rect(map_screen_w, 0, pyxel.width - map_screen_w, pyxel.height, self.outside_area_color)
        # 下側の余白
        if map_screen_h < pyxel.height:
            pyxel.rect(0, map_screen_h, pyxel.width, pyxel.height - map_screen_h, self.outside_area_color)
