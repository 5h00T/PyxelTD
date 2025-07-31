"""
ステージマスターデータ定義
"""

from typing import List
from .map_master import MAP_MASTER_LIST


class EnemySpawnData:
    """
    1体のエネミー出現情報
    """

    def __init__(self, time: int, enemy_type: str, spawn_point: tuple[int, int]):
        self.time = time  # 出現フレーム
        self.enemy_type = enemy_type  # "BasicEnemy"など
        self.spawn_point = spawn_point


class FlyingEnemySpawnData(EnemySpawnData):
    """
    飛行エネミー用の出現情報（着地地点を追加）
    """

    def __init__(self, time: int, spawn_point: tuple[int, int], landing_point: tuple[int, int]):
        super().__init__(time, "FlyingEnemy", spawn_point)
        self.landing_point = landing_point


class StageWaveData:
    """
    1ウェーブの出現情報
    """

    def __init__(self, spawns: List[EnemySpawnData]):
        self.spawns = spawns


class StageMasterData:
    """
    ステージ全体のマスターデータ
    """

    def __init__(self, map_id: int, map_data: list[list[int]], waves: List[StageWaveData]):
        self.map_id = map_id
        self.map_data = map_data  # 2次元リストのマップデータ
        self.waves = waves


# --- ステージごとのマスターデータリスト ---
STAGE_MASTER_LIST = [
    StageMasterData(
        map_id=1,
        map_data=MAP_MASTER_LIST[0],
        waves=[
            StageWaveData(
                [
                    *[EnemySpawnData(time=i * 60, enemy_type="BasicEnemy", spawn_point=(3, 0)) for i in range(5)],
                    *[
                        FlyingEnemySpawnData(
                            time=100 + i * 60,
                            spawn_point=(9, 0),
                            landing_point=(13, 6),
                        )
                        for i in range(5)
                    ],
                ]
            ),
            StageWaveData([]),
        ],
    ),
    StageMasterData(
        map_id=2,
        map_data=MAP_MASTER_LIST[1],
        waves=[
            StageWaveData(
                [
                    *[EnemySpawnData(time=i * 60, enemy_type="BasicEnemy", spawn_point=(0, 1)) for i in range(5)],
                    *[
                        EnemySpawnData(time=333 + i * 60, enemy_type="BasicEnemy", spawn_point=(16, 1))
                        for i in range(5)
                    ],
                    *[
                        EnemySpawnData(time=555 + i * 60, enemy_type="BasicEnemy", spawn_point=(14, 11))
                        for i in range(5)
                    ],
                ]
            ),
        ],
    ),
    StageMasterData(
        map_id=3,
        map_data=MAP_MASTER_LIST[2],
        waves=[
            StageWaveData(
                [
                    *[EnemySpawnData(time=i * 60, enemy_type="BasicEnemy", spawn_point=(0, 0)) for i in range(5)],
                ]
            ),
        ],
    ),
]
