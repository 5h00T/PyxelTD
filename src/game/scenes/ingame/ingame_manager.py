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

        # --- 所持資金 ---
        self.funds: int = 100  # 初期資金

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
            # --- ユニット選択UIをマップ表示領域の右側に縦並びで描画 ---
            ui_x = self.camera.view_width * TILE_SIZE  # マップ表示領域の右端
            ui_y = 0
            ui_w = game.WINDOW_WIDTH - ui_x  # 画面右端までの幅
            ui_h = game.WINDOW_HEIGHT  # 画面全体の高さ
            pyxel.rect(ui_x, ui_y, ui_w, ui_h, 5)  # UI背景

            # タイトル（中央寄せ）
            title_text = "ユニット選択"
            title_w = len(title_text) * 8
            title_x = ui_x + (ui_w - title_w) // 2
            FontRenderer.draw_text(title_x, ui_y + 4, title_text, 7, font_name="default")

            # ユニットリストの描画設定
            font_h = 8
            item_pad = 4  # 各ユニット間の余白
            item_h = font_h * 2 + item_pad  # 2行分＋余白
            list_top = ui_y + 16  # タイトル下からリスト開始

            # ユニットを縦に並べて描画
            for idx, unit in enumerate(self.unit_list):
                y = list_top + idx * item_h
                # 選択中はハイライト
                if idx == self.unit_ui_cursor:
                    pyxel.rect(ui_x + 2, y - 2, ui_w - 4, item_h, 6)
                # ユニット名（上段）
                FontRenderer.draw_text(
                    ui_x + 8, y + 2, f"{unit.name}", 1 if idx == self.unit_ui_cursor else 0, font_name="default"
                )
                # コスト（下段、左寄せ）
                cost_str = f"コスト: {unit.cost}"
                FontRenderer.draw_text(ui_x + 8, y + 2 + font_h, cost_str, 3, font_name="default")

            # 選択中ユニットの説明（下部に2行まで折り返し表示）
            sel_unit = self.unit_list[self.unit_ui_cursor]
            desc_y = ui_y + ui_h - 24
            max_desc_width = ui_w - 8  # 左右余白
            max_chars_per_line = max_desc_width // 8
            desc_lines = []
            desc = sel_unit.description
            while desc:
                desc_lines.append(desc[:max_chars_per_line])
                desc = desc[max_chars_per_line:]
            for i, line in enumerate(desc_lines[:2]):
                FontRenderer.draw_text(ui_x + 4, desc_y + i * 9, line, 13, font_name="default")

        # --- マップ領域下に資金を表示 ---
        map_bottom_y = self.camera.view_height * TILE_SIZE
        ui_x = 0
        ui_y = map_bottom_y
        ui_w = self.camera.view_width * TILE_SIZE
        ui_h = game.WINDOW_HEIGHT - map_bottom_y
        # 背景（薄いグレー）
        pyxel.rect(ui_x, ui_y, ui_w, ui_h, 13)
        # 資金テキスト
        funds = getattr(self, "funds", 100)
        funds_text = f"資金: {funds}"
        FontRenderer.draw_text(ui_x + 8, ui_y + 0, funds_text, 1, font_name="default")

        # --- Base HP表示 ---
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
