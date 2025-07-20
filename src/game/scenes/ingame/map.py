"""
Map - シンプルなマップタイル管理クラス
各タイルは8x8px、種別ごとに描画方法を分岐
"""

from typing import List

from typing import Optional

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
            width (int): マップ横タイル数（仮）
            height (int): マップ縦タイル数（仮）
        Note:
            実際のマップサイズは生成された2次元配列のサイズに合わせて自動設定されます。
        """
        self.data: List[List[int]] = self.generate_sample_stage(width, height)
        # 実際のマップサイズを配列から取得
        self.height = len(self.data)
        self.width = len(self.data[0]) if self.data else 0

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

    def draw(
        self, camera_x: int = 0, camera_y: int = 0, view_width: Optional[int] = None, view_height: Optional[int] = None
    ) -> None:
        """
        カメラ範囲のみマップを描画。
        Args:
            camera_x (int): カメラ左上タイルX
            camera_y (int): カメラ左上タイルY
            view_width (int): 画面表示タイル数X
            view_height (int): 画面表示タイル数Y
        """
        import pyxel
        from .constants import TILE_SIZE, VIEW_TILE_WIDTH, VIEW_TILE_HEIGHT

        view_width = view_width if view_width is not None else VIEW_TILE_WIDTH
        view_height = view_height if view_height is not None else VIEW_TILE_HEIGHT
        for y in range(camera_y, min(camera_y + view_height, self.height)):
            for x in range(camera_x, min(camera_x + view_width, self.width)):
                tile = self.data[y][x]
                px = (x - camera_x) * TILE_SIZE
                py = (y - camera_y) * TILE_SIZE
                if tile == TILE_PATH:
                    pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 5)  # 灰色
                elif tile == TILE_PLACEABLE:
                    pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 7)  # 白
                elif tile == TILE_BLOCKED:
                    pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 7)  # 白地
                    pyxel.line(px, py, px + TILE_SIZE - 1, py + TILE_SIZE - 1, 8)  # バツ印
                    pyxel.line(px + TILE_SIZE - 1, py, px, py + TILE_SIZE - 1, 8)
