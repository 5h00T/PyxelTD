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
        カーソルを移動する。画面外にはみ出さないよう制限。
        """
        self.x = max(0, min(self.x + dx, self.map_width - 1))
        self.y = max(0, min(self.y + dy, self.map_height - 1))
        print(f"Cursor moved to ({self.x}, {self.y})")

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

        screen_x = (self.x - camera_x) * 8
        screen_y = (self.y - camera_y) * 8
        if 0 <= screen_x < 8 * 14 and 0 <= screen_y < 8 * 14:
            pyxel.rectb(screen_x, screen_y, 8, 8, 10)  # 黄色枠
