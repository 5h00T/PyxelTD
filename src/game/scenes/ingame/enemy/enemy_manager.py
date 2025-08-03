"""
EnemyManager - 敵ユニットの管理クラス
"""

from typing import List
from .enemy import Enemy


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
