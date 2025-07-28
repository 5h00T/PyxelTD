"""
Bullet - ユニットの弾（攻撃）クラス
"""

from .enemy.enemy import Enemy


class Bullet:
    """
    ユニットの弾（攻撃）を表すクラス。
    敵に向かって移動し、当たるとダメージを与える。
    """

    def __init__(
        self,
        x: float,
        y: float,
        target: "Enemy",
        damage: int,
        speed: float = 0.5,
        aoe_radius: float = 0.0,
        flying_effect: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.target = target  # Enemyインスタンス
        self.damage = damage
        self.speed = speed
        self.aoe_radius = aoe_radius  # 範囲攻撃半径（0なら単体）
        self.is_active = True
        self.hit_pos = None  # type: tuple[float, float] | None
        self.flying_effect = flying_effect

    def update(self) -> None:
        """
        弾をターゲットに向けて移動。到達したらダメージを与える。
        """
        print(f"Updating bullet at ({self.x}, {self.y}) towards target at ({self.target.x}, {self.target.y})")
        if not self.is_active or not self.target.is_alive:
            self.is_active = False
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = (dx**2 + dy**2) ** 0.5
        if dist < self.speed or dist == 0:
            # 命中
            if self.aoe_radius > 0:
                # 範囲攻撃: 範囲内の敵全てにダメージ（Manager側で処理）
                self.hit_pos = (self.target.x, self.target.y)
            else:
                damage = self.damage
                if self.flying_effect:
                    # 飛行特効ならダメージを2倍
                    damage *= 2
                self.target.damage(damage)
            self.is_active = False
        else:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        弾を画面上に描画。
        """
        import pyxel
        from .constants import TILE_SIZE

        print(f"Drawing bullet at ({self.x}, {self.y})")
        sx = int((self.x - camera_x) * TILE_SIZE + TILE_SIZE // 2)
        sy = int((self.y - camera_y) * TILE_SIZE + TILE_SIZE // 2)
        pyxel.circ(sx, sy, 2, 7)
