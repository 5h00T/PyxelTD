from typing import List, Tuple, Callable, Optional
from .buff_manager import BuffManager
from .buff import BuffBase

"""
Enemy - 敵ユニットの基本クラス
"""

from abc import ABC, abstractmethod


class Enemy(ABC):
    """
    敵ユニットの抽象基底クラス。
    位置・速度・HP・移動・描画・到達判定などを管理。
    継承先で各メソッドを実装すること。
    """

    def __init__(
        self,
        x: float,
        y: float,
        base_speed: float,
        hp: int,
        path: list[Tuple[int, int]],
        reward: int = 5,
        on_defeat: Optional[Callable[["Enemy"], None]] = None,
        coefficient: float = 1.0,
    ) -> None:
        self.x = x
        self.y = y
        self.base_speed = base_speed
        self.max_hp = int(hp * coefficient)  # ステージ難易度調整用係数を適用
        self.hp = self.max_hp
        self.path = path
        self.path_index = 0
        self.is_alive = True  # Falseなら死亡・ゴール到達
        self.hp_bar_timer = 0  # HPバー表示タイマー（フレーム数）
        self.reward = int(reward * coefficient)  # 報酬も係数適用
        self.is_flying = False  # 飛行中かどうか
        self.on_defeat = on_defeat  # 敵撃破時のコールバック
        self.buff_manager = BuffManager()
        self.coefficient = coefficient

    def update(self) -> bool:
        """
        経路に沿って移動し、HPが0以下なら死亡。
        Returns:
            bool: 防衛拠点に到達したらTrue
        """
        self.buff_manager.update()
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
            if dist < self.get_speed():
                self.x = target_x
                self.y = target_y
                self.path_index += 1
            else:
                if dist != 0:
                    self.x += self.get_speed() * dx / dist
                    self.y += self.get_speed() * dy / dist
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
            if self.on_defeat:
                self.on_defeat(self)

    def is_goal(self) -> bool:
        """
        ゴール到達判定。
        Returns:
            bool: ゴールに到達したらTrue
        """
        return self.path_index >= len(self.path)

    def add_buff(self, buff: BuffBase) -> None:
        """
        バフを適用する。
        Args:
            buff: Buffインスタンス
        """
        self.buff_manager.add_buff(buff)

    def get_speed(self) -> float:
        """
        現在の移動速度を取得。
        バフによる速度変更があれば反映される。
        Returns:
            float: 現在の移動速度
        """
        return self.base_speed * self.buff_manager.get_speed_multiplier()


class BasicEnemy(Enemy):
    """
    標準的な敵ユニット。
    """

    DEFAULT_HP = 16
    DEFAULT_SPEED = 0.04
    DEFAULT_REWARD = 5
    COLOR = 8  # 赤

    def __init__(
        self,
        x: float,
        y: float,
        path: list[tuple[int, int]],
        on_defeat: Optional[Callable[["Enemy"], None]] = None,
        coefficient: float = 1.0,
    ) -> None:
        super().__init__(
            x,
            y,
            self.DEFAULT_SPEED,
            self.DEFAULT_HP,
            path,
            reward=self.DEFAULT_REWARD,
            on_defeat=on_defeat,
            coefficient=coefficient,
        )

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

    DEFAULT_HP = 10
    DEFAULT_SPEED = 0.09
    DEFAULT_REWARD = 4
    COLOR = 10  # 緑

    def __init__(
        self,
        x: float,
        y: float,
        path: list[tuple[int, int]],
        on_defeat: Optional[Callable[["Enemy"], None]] = None,
        coefficient: float = 1.0,
    ) -> None:
        super().__init__(
            x,
            y,
            self.DEFAULT_SPEED,
            self.DEFAULT_HP,
            path,
            reward=self.DEFAULT_REWARD,
            on_defeat=on_defeat,
            coefficient=coefficient,
        )

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

    DEFAULT_HP = 29
    DEFAULT_SPEED = 0.025
    DEFAULT_REWARD = 5
    COLOR = 12  # 紫

    def __init__(
        self,
        x: float,
        y: float,
        path: list[tuple[int, int]],
        on_defeat: Optional[Callable[["Enemy"], None]] = None,
        coefficient: float = 1.0,
    ) -> None:
        super().__init__(
            x,
            y,
            self.DEFAULT_SPEED,
            self.DEFAULT_HP,
            path,
            reward=self.DEFAULT_REWARD,
            on_defeat=on_defeat,
            coefficient=coefficient,
        )

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


class FlyingEnemy(Enemy):
    """
    飛行→着地→道を進む特殊エネミー。
    マップ外で生成され、指定座標まで直線飛行し、着地後は道を進む。
    """

    DEFAULT_HP = 22
    DEFAULT_SPEED = 0.05
    DEFAULT_REWARD = 6
    COLOR = 6  # 青

    def __init__(
        self,
        start_x: float,
        start_y: float,
        land_pos: Tuple[int, int],
        path: List[Tuple[int, int]],
        on_defeat: Optional[Callable[["Enemy"], None]] = None,
        coefficient: float = 1.0,
    ) -> None:
        """
        Args:
            start_x, start_y: マップ外の初期座標
            land_pos: 着地する道の座標 (タイル座標)
            path: 着地後に進む道のリスト
        """
        super().__init__(
            start_x,
            start_y,
            self.DEFAULT_SPEED,
            self.DEFAULT_HP,
            path,
            reward=self.DEFAULT_REWARD,
            on_defeat=on_defeat,
            coefficient=coefficient,
        )
        self.landing_x = land_pos[0]
        self.landing_y = land_pos[1]
        self.is_flying = True

    def update(self) -> bool:
        """
        飛行中は直線移動、着地後は道を進む。
        Returns:
            bool: ゴール到達時True
        """
        if not self.is_alive:
            return False
        if self.hp <= 0:
            self.is_alive = False
            return False
        if self.hp_bar_timer > 0:
            self.hp_bar_timer -= 1

        if self.is_flying:
            # 直線で着地点へ
            dx = self.landing_x - self.x
            dy = self.landing_y - self.y
            dist = (dx**2 + dy**2) ** 0.5
            if dist < self.get_speed():
                self.x = self.landing_x
                self.y = self.landing_y
                self.is_flying = False
                self.path_index = 0

            else:
                if dist != 0:
                    self.x += self.get_speed() * dx / dist
                    self.y += self.get_speed() * dy / dist
            return False
        else:
            # 着地後は通常の道エネミーと同じ
            return super().update()

    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        敵ユニットを画面上に描画。
        飛行中は羽付き、着地後は青丸。
        """
        import pyxel
        from ..constants import TILE_SIZE

        screen_x = int((self.x - camera_x) * TILE_SIZE)
        screen_y = int((self.y - camera_y) * TILE_SIZE)
        if self.is_alive:
            cx = screen_x + TILE_SIZE // 2
            cy = screen_y + TILE_SIZE // 2
            if self.is_flying:
                # --- 影（ディザAPI）描画 ---
                shadow_radius = 5
                shadow_cx = cx
                shadow_cy = cy + 10  # 本体より下
                pyxel.dither(0.3)
                pyxel.circ(shadow_cx, shadow_cy, shadow_radius, 0)
                pyxel.dither(1.0)  # ディザ解除（完全不透明）
                # --- 本体・羽 ---
                pyxel.circ(cx, cy, TILE_SIZE // 2, 7)
                pyxel.circ(cx, cy, TILE_SIZE // 2 - 2, self.COLOR)
                # 羽（左右に白い線）
                pyxel.line(cx - TILE_SIZE // 2, cy, cx - TILE_SIZE, cy - TILE_SIZE // 2, 7)
                pyxel.line(cx + TILE_SIZE // 2, cy, cx + TILE_SIZE, cy - TILE_SIZE // 2, 7)
            else:
                # 着地後は青い丸＋中央に点
                pyxel.circ(cx, cy, TILE_SIZE // 2, 7)
                pyxel.circ(cx, cy, TILE_SIZE // 2 - 2, self.COLOR)
                pyxel.pset(cx, cy, 0)
            if self.hp_bar_timer > 0 and self.max_hp > 0:
                bar_w = TILE_SIZE
                bar_h = 3
                bar_x = screen_x
                bar_y = screen_y + TILE_SIZE
                hp_ratio = max(0, self.hp) / self.max_hp
                filled_w = int(bar_w * hp_ratio)
                pyxel.rect(bar_x, bar_y, bar_w, bar_h, 0)
                pyxel.rect(bar_x, bar_y, filled_w, bar_h, 11)
