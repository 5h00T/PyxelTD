"""
Enemy - 敵ユニットの基本クラス
"""

from typing import Tuple


class Enemy:
    """
    敵ユニットの基本クラス。
    位置・速度・HP・移動・描画・到達判定などを管理。
    """

    def __init__(self, x: float, y: float, speed: float, hp: int, path: list[Tuple[int, int]]) -> None:
        """
        敵ユニットの初期化。
        Args:
            x (float): 初期X座標
            y (float): 初期Y座標
            speed (float): 移動速度（タイル/フレーム）
            hp (int): ヒットポイント
            path (list[Tuple[int, int]]): 進行経路（タイル座標リスト）
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.path = path
        self.path_index = 0  # 現在の経路インデックス
        self.is_alive = True

    def update(self) -> None:
        """
        毎フレーム呼び出し。経路に沿って移動。
        HPが0以下なら死亡。
        """
        if not self.is_alive:
            return
        if self.hp <= 0:
            self.is_alive = False
            return
        # 経路移動
        if self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx**2 + dy**2) ** 0.5
            if dist < self.speed:
                self.x = target_x
                self.y = target_y
                self.path_index += 1
            else:
                if dist != 0:
                    self.x += self.speed * dx / dist
                    self.y += self.speed * dy / dist
        else:
            # ゴール到達
            self.is_alive = False

    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        敵ユニットを画面上に描画。
        camera_x, camera_y: カメラの左上タイル座標
        """
        import pyxel
        from .constants import TILE_SIZE

        screen_x = int((self.x - camera_x) * TILE_SIZE)
        screen_y = int((self.y - camera_y) * TILE_SIZE)
        if self.is_alive:
            pyxel.circ(screen_x + TILE_SIZE // 2, screen_y + TILE_SIZE // 2, TILE_SIZE // 2, 8)  # 赤丸

    def damage(self, amount: int) -> None:
        """
        ダメージを受ける。
        Args:
            amount (int): ダメージ量
        """
        self.hp -= amount
        if self.hp <= 0:
            self.is_alive = False

    def is_goal(self) -> bool:
        """
        ゴール到達判定。
        Returns:
            bool: ゴールに到達したらTrue
        """
        return self.path_index >= len(self.path)
