"""
StageManager - ステージ進行・エネミー出現管理クラス
"""

from .stage_master import StageMasterData, EnemySpawnData, FlyingEnemySpawnData
from .enemy.enemy_manager import EnemyManager
from .enemy.enemy import BasicEnemy
from .enemy.enemy import Enemy
from .enemy.enemy import FastEnemy
from .enemy.enemy import TankEnemy
from .enemy.enemy import FlyingEnemy
from .map import Map


class StageManager:
    """
    ステージ進行・エネミー出現管理クラス。
    経過フレームを管理し、マスターデータに従いエネミーを出現させる。
    """

    def __init__(self, stage_master: StageMasterData, enemy_manager: EnemyManager, map: Map) -> None:
        self.stage_master = stage_master
        self.enemy_manager = enemy_manager
        self.map = map
        self.frame = 0
        self.wave_index = 0
        self.spawned_flags: set[tuple[int, int]] = set()  # (wave, spawn_idx)のタプル

    def update(self) -> None:
        """
        経過フレームを進め、出現タイミングのエネミーをスポーン
        """
        if self.wave_index >= len(self.stage_master.waves):
            return  # 全ウェーブ終了
        wave = self.stage_master.waves[self.wave_index]
        for idx, spawn in enumerate(wave.spawns):
            key = (self.wave_index, idx)
            if self.frame >= spawn.time and key not in self.spawned_flags:
                self.spawn_enemy(spawn)
                self.spawned_flags.add(key)
        # ウェーブ終了判定
        if all((self.wave_index, idx) in self.spawned_flags for idx in range(len(wave.spawns))):
            self.wave_index += 1
            self.frame = 0
            self.spawned_flags = set()
        else:
            self.frame += 1

    def spawn_enemy(self, spawn: EnemySpawnData) -> None:
        """
        マスターデータに従いエネミーを生成・EnemyManagerに追加
        """
        # 敵種ごとにクラスを分岐
        enemy: Enemy
        goal_point = self.map.get_goal()
        path = self.map.get_path(spawn.spawn_point, goal_point) if goal_point else []
        print(f"Spawning {spawn.enemy_type} at {spawn.spawn_point} with path {path} goal {goal_point}")
        if spawn.enemy_type == BasicEnemy.__name__:
            enemy = BasicEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path)
        elif spawn.enemy_type == FastEnemy.__name__:
            enemy = FastEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path)
        elif spawn.enemy_type == TankEnemy.__name__:
            enemy = TankEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path)
        elif isinstance(spawn, FlyingEnemySpawnData):
            flying_spawn_data = spawn
            enemy = FlyingEnemy(
                start_x=flying_spawn_data.spawn_point[0],
                start_y=flying_spawn_data.spawn_point[1],
                land_pos=flying_spawn_data.landing_point,
                path=self.map.get_path(flying_spawn_data.landing_point, goal=goal_point),
            )
        else:
            # 未知の敵種はBasicEnemyで代用
            enemy = BasicEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path)
        self.enemy_manager.spawn_enemy(enemy)
