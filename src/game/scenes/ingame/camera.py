"""
Camera - マップ表示範囲（カメラ）管理クラス
"""


class Camera:
    """
    マップの表示範囲（カメラ位置）を管理するクラス。
    """

    def __init__(self, map_width: int, map_height: int, view_width: int = 14, view_height: int = 14) -> None:
        self.map_width = map_width
        self.map_height = map_height
        self.view_width = view_width
        self.view_height = view_height
        self.x = 0  # 左上タイル座標
        self.y = 0

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
            self.y = min(self.map_height - self.view_height, cursor_y - self.view_height + margin + 1)

    def get_pos(self) -> tuple[int, int]:
        """
        カメラの左上タイル座標を返す。
        """
        return self.x, self.y
