"""
Enemy - 敵ユニットの基本クラス
"""

from typing import Tuple
from abc import ABC, abstractmethod


class Enemy(ABC):
    """
    敵ユニットの抽象基底クラス。
    位置・速度・HP・移動・描画・到達判定などを管理。
    継承先で各メソッドを実装すること。
    """

    def __init__(self, x: float, y: float, speed: float, hp: int, path: list[Tuple[int, int]]) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.max_hp = hp
        self.hp = hp
        self.path = path
        self.path_index = 0
        self.is_alive = True  # Falseなら死亡・ゴール到達
        self.hp_bar_timer = 0  # HPバー表示タイマー（フレーム数）

    @abstractmethod
    def update(self) -> bool:
        """
        毎フレーム呼び出し。経路に沿って移動。
        HPが0以下なら死亡。
        Returns:
            bool: 防衛拠点に到達したらTrue
        """
        pass

    @abstractmethod
    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        敵ユニットを画面上に描画。
        camera_x, camera_y: カメラの左上タイル座標
        """
        pass

    @abstractmethod
    def damage(self, amount: int) -> None:
        """
        ダメージを受ける。
        Args:
            amount (int): ダメージ量
        """
        pass

    @abstractmethod
    def is_goal(self) -> bool:
        """
        ゴール到達判定。
        Returns:
            bool: ゴールに到達したらTrue
        """
        pass


class BasicEnemy(Enemy):
    """
    テスト用の基本エネミー。
    既存の挙動をそのまま実装。
    """

    def update(self) -> bool:
        def update_path() -> None:
            if not self.is_alive:
                return
            if self.hp <= 0:
                self.is_alive = False
                return
            # HPバータイマー減少
            if self.hp_bar_timer > 0:
                self.hp_bar_timer -= 1
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
            return

        update_path()
        return self.is_goal()

    def draw(self, camera_x: int, camera_y: int) -> None:
        import pyxel
        from ..constants import TILE_SIZE

        screen_x = int((self.x - camera_x) * TILE_SIZE)
        screen_y = int((self.y - camera_y) * TILE_SIZE)
        if self.is_alive:
            pyxel.circ(screen_x + TILE_SIZE // 2, screen_y + TILE_SIZE // 2, TILE_SIZE // 2, 8)  # 赤丸
            # ダメージを受けてから一定時間HPバー表示
            if self.hp_bar_timer > 0 and self.max_hp > 0:
                bar_w = TILE_SIZE
                bar_h = 3
                bar_x = screen_x
                bar_y = screen_y + TILE_SIZE  # エネミーの下
                hp_ratio = max(0, self.hp) / self.max_hp
                filled_w = int(bar_w * hp_ratio)
                pyxel.rect(bar_x, bar_y, bar_w, bar_h, 0)  # 背景（黒）
                pyxel.rect(bar_x, bar_y, filled_w, bar_h, 11)  # HP部分（黄）

    def damage(self, amount: int) -> None:
        """
        指定ダメージを受ける。HPが0以下なら死亡。
        HPバー表示タイマーをリセット。
        """
        self.hp -= amount
        self.hp_bar_timer = 60  # 60フレーム（約1秒）HPバー表示
        if self.hp <= 0:
            self.is_alive = False

    def is_goal(self) -> bool:
        return self.path_index >= len(self.path)
