"""
EnemyManager - 敵ユニットの管理クラス
"""

from typing import List
from .enemy import Enemy
from ..map import Map


class EnemyManager:
    """
    複数の敵ユニットを一括管理するクラス。
    生成・更新・描画・削除を担当。
    """

    def __init__(self) -> None:
        """
        敵ユニットリストの初期化。
        """
        self.enemies: List[Enemy] = []

    def spawn_enemy(self, enemy: Enemy) -> None:
        """
        新しい敵ユニットを追加。
        Args:
            enemy (Enemy): 追加する敵ユニット
        """
        self.enemies.append(enemy)

    def update(self) -> List[Enemy]:
        """
        全ての敵ユニットを更新。死亡した敵はリストから除去。
        """
        goal_enemies = []
        for enemy in self.enemies:
            is_goal_reached = enemy.update()
            if is_goal_reached:
                goal_enemies.append(enemy)
        # 死亡・ゴール到達した敵を除去
        self.enemies = [e for e in self.enemies if e.is_alive and not e.is_goal()]
        return goal_enemies

    def draw(self, camera_x: int, camera_y: int) -> None:
        """
        全ての敵ユニットを描画。
        camera_x, camera_y: カメラの左上タイル座標
        """
        for enemy in self.enemies:
            enemy.draw(camera_x, camera_y)

    def clear(self) -> None:
        """
        全ての敵ユニットを削除。
        """
        self.enemies.clear()

    def spawn_sample_enemies(self, map_obj: Map) -> None:
        """
        サンプルエネミーを複数生成して追加。
        マップの複数経路に沿って移動する。
        Args:
            map_obj (Map): マップオブジェクト
        """
        from .enemy import BasicEnemy

        paths = map_obj.get_all_paths_from_entrances_to_goal()
        if not paths:
            return
        # 各経路ごとにエネミーを生成
        for path in paths:
            if not path:
                continue
            sx, sy = path[0]
            # 各入口から3体ずつ生成
            for i in range(3):
                enemy = BasicEnemy(x=sx, y=sy, speed=0.2 + 0.1 * i, hp=10 + 5 * i, path=path)
                self.spawn_enemy(enemy)
