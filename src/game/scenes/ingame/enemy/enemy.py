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

    def __init__(self, x: float, y: float, speed: float, hp: int, path: list[Tuple[int, int]], reward: int = 5) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.max_hp = hp
        self.hp = hp
        self.path = path
        self.path_index = 0
        self.is_alive = True  # Falseなら死亡・ゴール到達
        self.hp_bar_timer = 0  # HPバー表示タイマー（フレーム数）
        self.reward = reward  # 撃破時の資金増加量

    def update(self) -> bool:
        """
        経路に沿って移動し、HPが0以下なら死亡。
        Returns:
            bool: 防衛拠点に到達したらTrue
        """
        if not self.is_alive:
            return False
        if self.hp <= 0:
            self.is_alive = False
            return False
        if self.hp_bar_timer > 0:
            self.hp_bar_timer -= 1
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
            self.is_alive = False
        return self.is_goal()

    @abstractmethod
    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        敵ユニットを画面上に描画。
        camera_x, camera_y: カメラの左上タイル座標
        """
        pass

    def damage(self, amount: int) -> None:
        """
        ダメージを受ける。HPが0以下なら死亡。
        HPバー表示タイマーをリセット。
        """
        self.hp -= amount
        self.hp_bar_timer = 60
        if self.hp <= 0:
            self.is_alive = False

    def is_goal(self) -> bool:
        """
        ゴール到達判定。
        Returns:
            bool: ゴールに到達したらTrue
        """
        return self.path_index >= len(self.path)


class BasicEnemy(Enemy):
    """
    標準的な敵ユニット。
    """

    DEFAULT_HP = 15
    DEFAULT_SPEED = 0.05
    COLOR = 8  # 赤

    def __init__(self, x: float, y: float, path: list[tuple[int, int]]) -> None:
        super().__init__(x, y, self.DEFAULT_SPEED, self.DEFAULT_HP, path, reward=5)

    def draw(self, camera_x: int, camera_y: int) -> None:
        import pyxel
        from ..constants import TILE_SIZE

        screen_x = int((self.x - camera_x) * TILE_SIZE)
        screen_y = int((self.y - camera_y) * TILE_SIZE)
        if self.is_alive:
            # 赤い丸＋白縁＋中央に点
            cx = screen_x + TILE_SIZE // 2
            cy = screen_y + TILE_SIZE // 2
            pyxel.circ(cx, cy, TILE_SIZE // 2, 7)  # 白縁
            pyxel.circ(cx, cy, TILE_SIZE // 2 - 2, self.COLOR)  # 本体
            pyxel.pset(cx, cy, 0)  # 黒点
            if self.hp_bar_timer > 0 and self.max_hp > 0:
                bar_w = TILE_SIZE
                bar_h = 3
                bar_x = screen_x
                bar_y = screen_y + TILE_SIZE
                hp_ratio = max(0, self.hp) / self.max_hp
                filled_w = int(bar_w * hp_ratio)
                pyxel.rect(bar_x, bar_y, bar_w, bar_h, 0)
                pyxel.rect(bar_x, bar_y, filled_w, bar_h, 11)


class FastEnemy(Enemy):
    """
    高速移動型の敵ユニット。
    """

    DEFAULT_HP = 8
    DEFAULT_SPEED = 0.12
    COLOR = 10  # 緑

    def __init__(self, x: float, y: float, path: list[tuple[int, int]]) -> None:
        super().__init__(x, y, self.DEFAULT_SPEED, self.DEFAULT_HP, path, reward=8)

    def draw(self, camera_x: int, camera_y: int) -> None:
        import pyxel
        from ..constants import TILE_SIZE

        screen_x = int((self.x - camera_x) * TILE_SIZE)
        screen_y = int((self.y - camera_y) * TILE_SIZE)
        if self.is_alive:
            # 緑の三角形＋白縁
            cx = screen_x + TILE_SIZE // 2
            cy = screen_y + TILE_SIZE // 2
            size = TILE_SIZE // 2
            # 白縁
            pyxel.tri(cx, cy - size, cx - size, cy + size, cx + size, cy + size, 7)
            # 本体
            pyxel.tri(cx, cy - size + 2, cx - size + 2, cy + size - 2, cx + size - 2, cy + size - 2, self.COLOR)
            if self.hp_bar_timer > 0 and self.max_hp > 0:
                bar_w = TILE_SIZE
                bar_h = 3
                bar_x = screen_x
                bar_y = screen_y + TILE_SIZE
                hp_ratio = max(0, self.hp) / self.max_hp
                filled_w = int(bar_w * hp_ratio)
                pyxel.rect(bar_x, bar_y, bar_w, bar_h, 0)
                pyxel.rect(bar_x, bar_y, filled_w, bar_h, 11)


class TankEnemy(Enemy):
    """
    高耐久・低速型の敵ユニット。
    """

    DEFAULT_HP = 40
    DEFAULT_SPEED = 0.025
    COLOR = 12  # 紫

    def __init__(self, x: float, y: float, path: list[tuple[int, int]]) -> None:
        super().__init__(x, y, self.DEFAULT_SPEED, self.DEFAULT_HP, path, reward=15)

    def draw(self, camera_x: int, camera_y: int) -> None:
        import pyxel
        from ..constants import TILE_SIZE

        screen_x = int((self.x - camera_x) * TILE_SIZE)
        screen_y = int((self.y - camera_y) * TILE_SIZE)
        if self.is_alive:
            # Tank: 紫の大きな四角＋黒縁＋中央に小さい四角
            pyxel.rect(screen_x - 2, screen_y - 2, TILE_SIZE + 4, TILE_SIZE + 4, 0)  # 黒縁
            pyxel.rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE, self.COLOR)
            pyxel.rect(screen_x + TILE_SIZE // 4, screen_y + TILE_SIZE // 4, TILE_SIZE // 2, TILE_SIZE // 2, 7)  # 白
            if self.hp_bar_timer > 0 and self.max_hp > 0:
                bar_w = TILE_SIZE
                bar_h = 3
                bar_x = screen_x
                bar_y = screen_y + TILE_SIZE
                hp_ratio = max(0, self.hp) / self.max_hp
                filled_w = int(bar_w * hp_ratio)
                pyxel.rect(bar_x, bar_y, bar_w, bar_h, 0)
                pyxel.rect(bar_x, bar_y, filled_w, bar_h, 11)
