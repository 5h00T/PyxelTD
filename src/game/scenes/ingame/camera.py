"""
Camera - マップ表示範囲（カメラ）管理クラス
"""

from typing import Optional, Tuple


class Camera:
    """
    マップの表示範囲（カメラ位置）を管理するクラス。
    """

    def __init__(
        self,
        init_position: Tuple[int, int],
        map_width: int,
        map_height: int,
        view_width: Optional[int] = None,
        view_height: Optional[int] = None,
    ) -> None:
        from .constants import VIEW_TILE_WIDTH, VIEW_TILE_HEIGHT

        self.map_width = map_width
        self.map_height = map_height
        self.view_width = view_width if view_width is not None else VIEW_TILE_WIDTH
        self.view_height = view_height if view_height is not None else VIEW_TILE_HEIGHT
        # init_positionが中央に来るように調整
        self.x = init_position[0] - self.view_width // 2
        self.y = init_position[1] - self.view_height // 2
        self.x, self.y = self.clamp_position(self.x, self.y)

    def move_to_cursor(self, cursor_x: int, cursor_y: int) -> None:
        """
        カーソルが画面端に来たらカメラを移動。
        """
        # カーソルが画面端（3タイル分）に近づいたらカメラを動かす
        margin = 2
        # X方向
        if cursor_x < self.x + margin:
            self.x = max(0, cursor_x - margin)
        elif cursor_x >= self.x + self.view_width - margin:
            self.x = min(self.map_width - self.view_width, cursor_x - self.view_width + margin + 1)
        # Y方向
        if cursor_y < self.y + margin:
            self.y = max(0, cursor_y - margin)
        elif cursor_y >= self.y + self.view_height - margin:
            self.y = max(min(self.map_height - self.view_height, cursor_y - self.view_height + margin + 1), 0)

    def clamp_position(self, x: int, y: int) -> Tuple[int, int]:
        """
        カメラ位置をマップの範囲内に制限。
        """
        clamped_x = max(0, min(x, self.map_width - self.view_width))
        clamped_y = max(0, min(y, self.map_height - self.view_height))
        return clamped_x, clamped_y

    def get_pos(self) -> tuple[int, int]:
        """
        カメラの左上タイル座標を返す。
        """
        return self.x, self.y
