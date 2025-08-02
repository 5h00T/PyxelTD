from typing import Callable
from .stage_master import StageMasterData, EnemySpawnData, FlyingEnemySpawnData, StageWaveData, Delay
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
        self.wave_index = 0
        self.spawn_index = 0  # 現在のspawnsリストのインデックス
        self.delay_counter = 0  # Delay用カウンタ

    def update(self, on_defeat: Callable) -> bool:
        """
        ウェーブ進行・エネミー出現管理。
        spawnsリストを順次処理し、Delayなら待機、EnemySpawnDataなら即スポーン。
        ウェーブ内の全ての敵が死亡したらウェーブ完了とする。
        """
        if self.wave_index >= len(self.stage_master.waves):
            # 全ウェーブ終了
            return True
        wave = self.stage_master.waves[self.wave_index]
        spawns = wave.spawns

        # spawnsリストを順次処理
        while self.spawn_index < len(spawns):
            spawn = spawns[self.spawn_index]
            if isinstance(spawn, Delay):
                if self.delay_counter < spawn.frame:
                    self.delay_counter += 1
                    break  # Delay中はここで止める
                else:
                    self.delay_counter = 0
                    self.spawn_index += 1
            elif isinstance(spawn, (EnemySpawnData, FlyingEnemySpawnData)):
                self.spawn_enemy(spawn, on_defeat)
                self.spawn_index += 1
            else:
                # 未知の型はスキップ
                self.spawn_index += 1

        # ウェーブ完了判定
        if self._is_wave_complete(wave):
            self.wave_index += 1
            self.spawn_index = 0
            self.delay_counter = 0
        return False

    def _is_wave_complete(self, wave: StageWaveData) -> bool:
        """
        ウェーブ内の全てのspawnsを処理し終え、かつ全ての敵が死亡したらTrue
        """
        all_spawned = self.spawn_index >= len(wave.spawns)
        all_dead = len(self.enemy_manager.enemies) == 0
        return all_spawned and all_dead

    def spawn_enemy(self, spawn: EnemySpawnData, onDefeat: Callable) -> None:
        """
        マスターデータに従いエネミーを生成・EnemyManagerに追加
        """
        enemy: Enemy
        goal_point = self.map.get_goal()
        path = self.map.get_path(spawn.spawn_point, goal_point) if goal_point else []
        if spawn.enemy_type == BasicEnemy.__name__:
            enemy = BasicEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path, on_defeat=onDefeat)
        elif spawn.enemy_type == FastEnemy.__name__:
            enemy = FastEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path, on_defeat=onDefeat)
        elif spawn.enemy_type == TankEnemy.__name__:
            enemy = TankEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path, on_defeat=onDefeat)
        elif isinstance(spawn, FlyingEnemySpawnData):
            flying_spawn_data = spawn
            enemy = FlyingEnemy(
                start_x=flying_spawn_data.spawn_point[0],
                start_y=flying_spawn_data.spawn_point[1],
                land_pos=flying_spawn_data.landing_point,
                path=self.map.get_path(flying_spawn_data.landing_point, goal=goal_point),
                on_defeat=onDefeat,
            )
        else:
            # 未知の敵種はBasicEnemyで代用
            enemy = BasicEnemy(x=spawn.spawn_point[0], y=spawn.spawn_point[1], path=path, on_defeat=onDefeat)
        self.enemy_manager.spawn_enemy(enemy)
