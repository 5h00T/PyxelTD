"""
Bullet - ユニットの弾（攻撃）クラス
"""

from .enemy.enemy import Enemy
from .enemy.buff import BuffBase


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
        grant_buff: BuffBase | None = None,
        speed: float = 0.5,
        aoe_radius: float = 0.0,
        flying_effect: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.target = target  # Enemyインスタンス
        self.damage = damage
        self.grant_buff = grant_buff
        self.speed = speed
        self.aoe_radius = aoe_radius  # 範囲攻撃半径（0なら単体）
        self.is_active = True
        self.hit_pos = None  # type: tuple[float, float] | None
        self.flying_effect = flying_effect

    def update(self, enemies: list[Enemy]) -> None:
        """
        弾をターゲットに向けて移動。到達したらダメージを与える。
        """

        def apply_damage(enemy: Enemy) -> None:
            damage = self.damage
            if self.flying_effect and enemy.is_flying:
                # 飛行特効ならダメージを2倍
                damage *= 2
            enemy.damage(damage)
            if self.grant_buff:
                enemy.buff_manager.add_buff(self.grant_buff)

        if not self.is_active or not self.target.is_alive:
            self.is_active = False
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = (dx**2 + dy**2) ** 0.5
        # 命中
        if dist < self.speed or dist == 0:
            # 範囲攻撃なら敵全てにダメージ
            if self.aoe_radius > 0:
                self.hit_pos = (self.target.x, self.target.y)
                # 範囲攻撃弾の着弾処理
                if self.aoe_radius > 0 and self.hit_pos is not None:
                    bx, by = self.hit_pos
                    for enemy in enemies:
                        if not enemy.is_alive:
                            continue
                        ex, ey = enemy.x, enemy.y
                        dist = ((ex - bx) ** 2 + (ey - by) ** 2) ** 0.5
                        if dist <= self.aoe_radius:
                            apply_damage(enemy)
                    self.hit_pos = None  # 1回だけ処理
            else:
                apply_damage(self.target)
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

        sx = int((self.x - camera_x) * TILE_SIZE + TILE_SIZE // 2)
        sy = int((self.y - camera_y) * TILE_SIZE + TILE_SIZE // 2)
        pyxel.circ(sx, sy, 2, 7)
