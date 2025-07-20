"""
Cursor - マップ上のカーソル管理クラス
"""

from typing import Tuple


class Cursor:
    """
    マップ上のカーソル位置・移動・描画を管理するクラス。
    """

    def __init__(self, map_width: int, map_height: int) -> None:
        self.x = 0
        self.y = 0
        self.map_width = map_width
        self.map_height = map_height

    def move(self, dx: int, dy: int) -> None:
        """
        カーソルを移動する。マップ外にはみ出さないよう制限。
        カメラがスクロールすることで、画面下端でもカーソルが移動可能。
        """
        new_x = self.x + dx
        new_y = self.y + dy
        # マップ全体の範囲で制限
        self.x = max(0, min(new_x, self.map_width - 1))
        self.y = max(0, min(new_y, self.map_height - 1))
        # デバッグ出力削除

    def get_pos(self) -> Tuple[int, int]:
        """
        カーソルの現在位置（タイル座標）を返す。
        """
        return self.x, self.y

    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        カーソルを画面上に描画。
        camera_x, camera_y: カメラの左上タイル座標
        """
        import pyxel
        from .constants import TILE_SIZE, VIEW_TILE_WIDTH, VIEW_TILE_HEIGHT

        screen_x = (self.x - camera_x) * TILE_SIZE
        screen_y = (self.y - camera_y) * TILE_SIZE
        if 0 <= screen_x < TILE_SIZE * VIEW_TILE_WIDTH and 0 <= screen_y < TILE_SIZE * VIEW_TILE_HEIGHT:
            pyxel.rectb(screen_x, screen_y, TILE_SIZE, TILE_SIZE, 10)  # 黄色枠
