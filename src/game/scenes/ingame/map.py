"""
Map - シンプルなマップタイル管理クラス
各タイルは8x8px、種別ごとに描画方法を分岐
"""

from typing import List

# タイル種別定数
TILE_PATH = 0  # 敵の道（灰色）
TILE_PLACEABLE = 1  # ユニット配置可能（白）
TILE_BLOCKED = 2  # ユニット配置不可（バツ印）


class Map:
    """
    マップタイル管理クラス。
    2次元リストでマップデータを保持。
    """

    def __init__(self, width: int, height: int) -> None:
        """
        マップ初期化。仮ステージデータ生成。
        Args:
            width (int): マップ横タイル数
            height (int): マップ縦タイル数
        """
        self.width = width
        self.height = height
        self.data: List[List[int]] = self.generate_sample_stage(width, height)

    @staticmethod
    def generate_sample_stage(width: int, height: int) -> List[List[int]]:
        """
        仮ステージ用のマップデータ生成。
        - 中央に道
        - 周囲は配置可
        - 右下は配置不可
        """
        data = [
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        return data

    def draw(self, camera_x: int = 0, camera_y: int = 0, view_width: int = 14, view_height: int = 14) -> None:
        """
        カメラ範囲のみマップを描画。
        Args:
            camera_x (int): カメラ左上タイルX
            camera_y (int): カメラ左上タイルY
            view_width (int): 画面表示タイル数X
            view_height (int): 画面表示タイル数Y
        """
        import pyxel

        for y in range(camera_y, min(camera_y + view_height, self.height)):
            for x in range(camera_x, min(camera_x + view_width, self.width)):
                tile = self.data[y][x]
                px = (x - camera_x) * 8
                py = (y - camera_y) * 8
                if tile == TILE_PATH:
                    pyxel.rect(px, py, 8, 8, 5)  # 灰色
                elif tile == TILE_PLACEABLE:
                    pyxel.rect(px, py, 8, 8, 7)  # 白
                elif tile == TILE_BLOCKED:
                    pyxel.rect(px, py, 8, 8, 7)  # 白地
                    pyxel.line(px, py, px + 7, py + 7, 8)  # バツ印
                    pyxel.line(px + 7, py, px, py + 7, 8)
