"""
PlayerUnit - プレイヤーが配置するユニットの基底クラスとマスターデータ
"""

from typing import List


class PlayerUnit:
    def get_upgrade_cost(self, level: int) -> int:
        """
        次のレベルへの強化コストを返す。強化不可の場合は0を返す。
        level: 現在のレベル（1始まり）
        """
        idx = min(level, len(self.upgrade_cost) - 1)
        if level >= self.max_level:
            return 0
        return self.upgrade_cost[idx]

    """
    プレイヤーユニットの基底クラス。
    攻撃力・射程・コスト・レベル・範囲攻撃フラグ等を持つ。
    """

    def __init__(
        self,
        unit_id: int,
        name: str,
        icon: int,
        description: str,
        cost: int,
        upgrade_cost: List[int],
        attack: List[int],
        range: List[int],
        attack_interval: int = 30,
        is_aoe: bool = False,
        max_level: int = 5,
        shape: str = "rect",
        level_colors: List[int] = [],
        flying_effect: bool = False,
    ) -> None:
        self.unit_id = unit_id
        self.name = name
        self.icon = icon
        self.description = description
        self.cost = cost
        self.upgrade_cost = upgrade_cost
        self.attack = attack  # レベルごとの攻撃力 [lv1, lv2, ...]
        self.range = range  # レベルごとの射程 [lv1, lv2, ...]
        self.attack_interval = attack_interval  # 発射間隔（フレーム数）
        self.is_aoe = is_aoe
        self.max_level = max_level
        self.shape = shape  # rect/tri/circ など
        self.level_colors = level_colors
        self.flying_effect = flying_effect

    def get_color(self, level: int) -> int:
        """
        指定レベルの色を返す。範囲外は最大レベル色。
        """
        idx = min(level - 1, len(self.level_colors) - 1)
        return self.level_colors[idx]

    def draw(self, x: int, y: int, level: int, tile_size: int) -> None:
        """
        ユニットの見た目を描画する。x, yはピクセル座標。
        レベルごとの色で描画。
        """
        import pyxel

        color = self.get_color(level)
        if self.shape == "rect":
            pyxel.rect(x, y, tile_size, tile_size, color)
        elif self.shape == "tri":
            pyxel.tri(x, y + tile_size, x + tile_size // 2, y, x + tile_size, y + tile_size, color)
        elif self.shape == "circ":
            pyxel.circ(x + tile_size // 2, y + tile_size // 2, tile_size // 2, color)
        else:
            pyxel.rect(x, y, tile_size, tile_size, color)

    def get_attack(self, level: int) -> int:
        """現在レベルの攻撃力を返す。"""
        idx = min(level - 1, len(self.attack) - 1)
        return self.attack[idx]

    def get_range(self, level: int) -> int:
        """現在レベルの射程を返す。"""
        idx = min(level - 1, len(self.range) - 1)
        return self.range[idx]


# --- ユニットマスターデータ ---
PLAYER_UNIT_MASTER: List[PlayerUnit] = [
    PlayerUnit(
        unit_id=1,
        name="槍兵",
        icon=0,
        description="近距離攻撃ユニット",
        cost=10,
        upgrade_cost=[10, 20, 40, 50, 100],
        attack=[10, 15, 20, 25, 30],
        range=[1, 1, 1, 1, 1],
        attack_interval=30,
        is_aoe=False,
        shape="rect",
        level_colors=[3, 11, 12, 10, 8],
    ),
    PlayerUnit(
        unit_id=2,
        name="弓兵",
        icon=1,
        description="飛行特効ユニット",
        cost=20,
        upgrade_cost=[20, 40, 80, 160, 320],
        attack=[10, 20, 30, 25, 30],
        range=[3, 3, 4, 4, 6],
        attack_interval=50,
        is_aoe=False,
        shape="tri",
        level_colors=[3, 11, 12, 10, 8],
        flying_effect=True,
    ),
    PlayerUnit(
        unit_id=3,
        name="魔法使い",
        icon=2,
        description="範囲攻撃ユニット",
        cost=150,
        upgrade_cost=[200, 400, 700, 800, 1000],
        attack=[25, 40, 50, 60, 60],
        range=[8, 8, 8, 8, 11],
        attack_interval=200,
        is_aoe=True,
        shape="circ",
        level_colors=[3, 11, 12, 10, 8],
    ),
]
