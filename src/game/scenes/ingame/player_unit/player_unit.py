from typing import List, Optional


class PlayerUnit:
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
        level_colors: Optional[List[int]] = None,
        flying_effect: bool = False,
        grants_slow: bool = False,
    ) -> None:
        """
        プレイヤーユニットの基底クラス。
        grants_slow: 攻撃時にスロウ効果を付与するかどうか
        """
        self.unit_id = unit_id
        self.name = name
        self.icon = icon
        self.description = description
        self.cost = cost
        self.upgrade_cost = upgrade_cost
        self.attack = attack
        self.range = range
        self.attack_interval = attack_interval
        self.is_aoe = is_aoe
        self.max_level = max_level
        self.shape = shape
        self.level_colors = level_colors if level_colors is not None else []
        self.flying_effect = flying_effect
        self.grants_slow = grants_slow

    def get_upgrade_cost(self, level: int) -> int:
        idx = min(level, len(self.upgrade_cost) - 1)
        if level >= self.max_level:
            return 0
        return self.upgrade_cost[idx]

    def get_color(self, level: int) -> int:
        idx = min(level - 1, len(self.level_colors) - 1)
        return self.level_colors[idx]

    def draw(self, x: int, y: int, level: int, tile_size: int) -> None:
        import pyxel

        color = self.get_color(level)
        if self.shape == "rect":
            pyxel.rect(x, y, tile_size, tile_size, color)
        elif self.shape == "tri":
            pyxel.tri(x, y + tile_size, x + tile_size // 2, y, x + tile_size, y + tile_size, color)
        elif self.shape == "circ":
            pyxel.circ(x + tile_size // 2, y + tile_size // 2, tile_size // 2, color)
        elif self.shape == "diamond":
            # ひし形（ダイヤ型）: 4頂点
            cx = x + tile_size // 2
            cy = y + tile_size // 2
            top = (cx, y)
            right = (x + tile_size, cy)
            bottom = (cx, y + tile_size)
            left = (x, cy)
            # 塗りつぶし（2三角形で分割）
            pyxel.tri(*top, *right, *bottom, color)
            pyxel.tri(*top, *bottom, *left, color)
            # 枠線
            pyxel.line(*top, *right, 7)
            pyxel.line(*right, *bottom, 7)
            pyxel.line(*bottom, *left, 7)
            pyxel.line(*left, *top, 7)
        else:
            pyxel.rect(x, y, tile_size, tile_size, color)

    def get_attack(self, level: int) -> int:
        idx = min(level - 1, len(self.attack) - 1)
        return self.attack[idx]

    def get_range(self, level: int) -> int:
        idx = min(level - 1, len(self.range) - 1)
        return self.range[idx]


# --- ユニットマスターデータ ---

PLAYER_UNIT_MASTER: List[PlayerUnit] = [
    PlayerUnit(
        unit_id=1,
        name="ソルジャー",
        icon=0,
        description="近距離攻撃",
        cost=10,
        upgrade_cost=[10, 20, 40, 50, 100],
        attack=[7, 14, 20, 25, 30],
        range=[1, 1, 1, 1, 1],
        attack_interval=35,
        is_aoe=False,
        shape="rect",
        level_colors=[3, 11, 12, 10, 8],
    ),
    PlayerUnit(
        unit_id=2,
        name="レンジャー",
        icon=1,
        description="飛行中の敵に特効",
        cost=20,
        upgrade_cost=[20, 40, 80, 160, 320],
        attack=[10, 20, 30, 25, 30],
        range=[3, 3, 4, 4, 6],
        attack_interval=60,
        is_aoe=False,
        shape="tri",
        level_colors=[3, 11, 12, 10, 8],
        flying_effect=True,
    ),
    PlayerUnit(
        unit_id=4,
        name="メイジ",
        icon=3,
        description="ヒットした敵を遅くする",
        cost=40,
        upgrade_cost=[40, 80, 160, 320, 560],
        attack=[7, 14, 28, 35, 45],
        range=[2, 3, 4, 5, 6],
        attack_interval=65,
        is_aoe=False,
        shape="circ",
        level_colors=[3, 11, 12, 10, 8],
        flying_effect=False,
        grants_slow=True,
    ),
    PlayerUnit(
        unit_id=3,
        name="ウィザード",
        icon=2,
        description="範囲攻撃",
        cost=150,
        upgrade_cost=[200, 400, 700, 800, 1000],
        attack=[20, 26, 33, 40, 40],
        range=[6, 6, 6, 6, 8],
        attack_interval=200,
        is_aoe=True,
        shape="diamond",
        level_colors=[3, 11, 12, 10, 8],
    ),
]
