"""
StageManager - ステージ進行・エネミー出現管理クラス
"""

from .stage_master import StageMasterData, EnemySpawnData
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
        path = self.stage_master.paths[spawn.path_id]
        # 敵種ごとにクラスを分岐
        enemy: Enemy
        if spawn.enemy_type == BasicEnemy.__name__:
            enemy = BasicEnemy(x=path[0][0], y=path[0][1], path=path)
        elif spawn.enemy_type == FastEnemy.__name__:
            enemy = FastEnemy(x=path[0][0], y=path[0][1], path=path)
        elif spawn.enemy_type == TankEnemy.__name__:
            enemy = TankEnemy(x=path[0][0], y=path[0][1], path=path)
        elif spawn.enemy_type == FlyingEnemy.__name__:
            # マップ外(-2, y)からpath[0]へ飛行し、着地後は道を進む
            print(f"Spawning FlyingEnemy at {path}")
            # TODO: 着地位置はマスターデータから取得する
            # TODO: 生成位置はマスターデータから取得する
            enemy = FlyingEnemy(
                start_x=-2, start_y=path[0][1], land_pos=(13, 6), path=self.map.get_path((13, 6), path[-1])
            )
        else:
            # 未知の敵種はBasicEnemyで代用
            enemy = BasicEnemy(x=path[0][0], y=path[0][1], path=path)
        self.enemy_manager.spawn_enemy(enemy)
