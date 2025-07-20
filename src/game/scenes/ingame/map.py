"""
Map - シンプルなマップタイル管理クラス
各タイルは8x8px、種別ごとに描画方法を分岐
"""

import pyxel
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
        data = [[TILE_PATH if x == width // 2 else TILE_PLACEABLE for x in range(width)] for y in range(height)]
        data[height - 1][width - 1] = TILE_BLOCKED
        return data

    def draw(self, offset_x: int = 0, offset_y: int = 0) -> None:
        """
        マップ全体を描画。
        Args:
            offset_x (int): 描画開始X座標
            offset_y (int): 描画開始Y座標
        """
        for y in range(self.height):
            for x in range(self.width):
                tile = self.data[y][x]
                px = offset_x + x * 8
                py = offset_y + y * 8
                if tile == TILE_PATH:
                    pyxel.rect(px, py, 8, 8, 5)  # 灰色
                elif tile == TILE_PLACEABLE:
                    pyxel.rect(px, py, 8, 8, 7)  # 白
                elif tile == TILE_BLOCKED:
                    pyxel.rect(px, py, 8, 8, 7)  # 白地
                    pyxel.line(px, py, px + 7, py + 7, 8)  # バツ印
                    pyxel.line(px + 7, py, px, py + 7, 8)
