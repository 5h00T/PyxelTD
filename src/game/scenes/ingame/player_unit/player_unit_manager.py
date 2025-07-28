"""
PlayerUnitManager - プレイヤーユニットの配置・管理・攻撃処理を担当
"""

from typing import Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..ingame_manager import InGameManager
from .player_unit import PlayerUnit
from ..enemy.enemy_manager import EnemyManager


class PlayerUnitInstance:
    """
    マップ上に配置されたプレイヤーユニットのインスタンス。
    各インスタンスはレベル・座標・攻撃クールダウン等を持つ。
    """

    def __init__(self, unit: PlayerUnit, pos: Tuple[int, int]) -> None:
        self.unit = unit
        self.pos = pos  # (x, y)
        self.level = 1
        self.cooldown = 0  # 予備
        self.attack_cooldown = 0  # 攻撃間隔管理

    def level_up(self) -> None:
        if self.level < self.unit.max_level:
            self.level += 1


class PlayerUnitManager:
    """
    プレイヤーユニットの配置・管理・攻撃処理を一元管理するクラス。
    """

    def __init__(self) -> None:
        self.units: Dict[Tuple[int, int], PlayerUnitInstance] = {}
        from ..bullet import Bullet

        self.bullets: list[Bullet] = []

        # --- 強化UI状態管理 ---
        self.is_upgrading_unit: bool = False  # 強化UI表示中か
        self.upgrade_ui_cursor: int = 0  # 0:強化 1:キャンセル
        self.selected_unit_pos: tuple[int, int] | None = None  # 強化対象ユニット座標

    def open_upgrade_ui(self, pos: tuple[int, int]) -> None:
        """
        指定座標のユニットの強化UIを開く。
        """
        if pos in self.units:
            self.is_upgrading_unit = True
            self.upgrade_ui_cursor = 1
            self.selected_unit_pos = pos

    def close_upgrade_ui(self) -> None:
        """
        強化UIを閉じる。
        """
        self.is_upgrading_unit = False
        self.upgrade_ui_cursor = 0
        self.selected_unit_pos = None

    def place_unit(self, unit: PlayerUnit, x: int, y: int) -> bool:
        """
        指定座標にユニットを配置。
        既に配置済みならFalse。
        """
        if (x, y) in self.units:
            return False
        self.units[(x, y)] = PlayerUnitInstance(unit, (x, y))
        return True

    def level_up_unit(self, x: int, y: int) -> bool:
        """
        指定座標のユニットをレベルアップ。
        最大レベルなら何もしない。
        """
        if (x, y) not in self.units:
            return False
        self.units[(x, y)].level_up()
        return True

    def update(self, enemy_manager: "EnemyManager", ingame_manager: "InGameManager") -> None:
        """
        全ユニットの攻撃処理・弾の更新を行う。
        """
        from ..bullet import Bullet

        # 弾の更新・消滅処理
        for bullet in self.bullets:
            bullet.update()

        # 範囲攻撃弾の着弾処理
        # 単体攻撃はバレット側で行っているので範囲攻撃もバレット側でいいかも
        for bullet in self.bullets:
            if bullet.aoe_radius > 0 and bullet.hit_pos is not None:
                bx, by = bullet.hit_pos
                for enemy in enemy_manager.enemies:
                    if not enemy.is_alive:
                        continue
                    ex, ey = enemy.x, enemy.y
                    dist = ((ex - bx) ** 2 + (ey - by) ** 2) ** 0.5
                    if dist <= bullet.aoe_radius:
                        damage = bullet.damage
                        if bullet.flying_effect:
                            # 飛行特効ならダメージを2倍
                            damage *= 2
                        enemy.damage(damage)
                bullet.hit_pos = None  # 1回だけ処理

        # --- 敵撃破時の資金加算 ---
        if ingame_manager is not None:
            for enemy in enemy_manager.enemies:
                if not enemy.is_alive and not hasattr(enemy, "_reward_given"):
                    ingame_manager.funds += getattr(enemy, "reward", 5)
                    setattr(enemy, "_reward_given", True)

        self.bullets = [b for b in self.bullets if b.is_active]

        # 各ユニットの攻撃判定
        for inst in self.units.values():
            if not hasattr(inst, "attack_cooldown"):
                inst.attack_cooldown = 0
            if inst.attack_cooldown > 0:
                inst.attack_cooldown -= 1
                continue
            # 射程内の敵を検索
            attack_range = inst.unit.get_range(inst.level)
            attack_power = inst.unit.get_attack(inst.level)
            cx, cy = inst.pos
            targets = []
            for enemy in enemy_manager.enemies:
                if not enemy.is_alive:
                    continue
                ex, ey = enemy.x, enemy.y
                dist = ((ex - cx) ** 2 + (ey - cy) ** 2) ** 0.5
                if dist <= attack_range:
                    targets.append(enemy)
            if not targets:
                continue
            if inst.unit.is_aoe:
                # 範囲攻撃: 射程内全てに弾
                for t in targets:
                    self.bullets.append(
                        Bullet(cx, cy, t, attack_power, aoe_radius=1.5, flying_effect=inst.unit.flying_effect)
                    )
            else:
                # 単体攻撃: 最初の敵に弾
                self.bullets.append(Bullet(cx, cy, targets[0], attack_power, flying_effect=inst.unit.flying_effect))
            inst.attack_cooldown = 30  # 仮: 30フレームごとに攻撃

    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        マップ上のユニットを描画する。
        """
        from ..constants import TILE_SIZE

        for inst in self.units.values():
            sx = (inst.pos[0] - camera_x) * TILE_SIZE
            sy = (inst.pos[1] - camera_y) * TILE_SIZE
            inst.unit.draw(sx, sy, inst.level, TILE_SIZE)

        # 弾の描画
        for bullet in self.bullets:
            bullet.draw(camera_x, camera_y)
