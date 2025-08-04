"""
PlayerUnitManager - プレイヤーユニットの配置・管理・攻撃処理を担当
"""

from typing import Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..ingame_manager import InGameManager
from .player_unit import PlayerUnit
from ..enemy.enemy_manager import EnemyManager
from ..enemy.buff import SpeedDownBuff


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
            bullet.update(enemy_manager.enemies)

        self.bullets = [b for b in self.bullets if b.is_active]

        # 各ユニットの攻撃判定
        for inst in self.units.values():
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
            # 単体攻撃: 最初の敵に弾
            grant_buff = None
            if inst.unit.grants_slow:
                grant_buff = SpeedDownBuff(duration=300, speed_multiplier=0.5)
            if inst.unit.is_aoe:
                # 範囲攻撃
                self.bullets.append(
                    Bullet(cx, cy, targets[0], attack_power, aoe_radius=2.5, flying_effect=inst.unit.flying_effect)
                )
            else:
                # 単体攻撃
                self.bullets.append(
                    Bullet(
                        cx,
                        cy,
                        targets[0],
                        attack_power,
                        grant_buff=grant_buff,
                        flying_effect=inst.unit.flying_effect,
                    )
                )

            inst.attack_cooldown = inst.unit.attack_interval  # ユニットごとの発射間隔

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
