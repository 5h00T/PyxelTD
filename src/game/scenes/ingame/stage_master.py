"""
ステージマスターデータ定義
"""

from typing import List


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

    def __init__(self, map_id: int, waves: List[StageWaveData]):
        self.map_id = map_id
        self.waves = waves


# --- サンプルデータ ---
SAMPLE_STAGE_MASTER = StageMasterData(
    map_id=1,
    waves=[
        StageWaveData(
            [
                # 5体のBasicEnemyを0,60,120,180,240フレームで出現
                *[EnemySpawnData(time=i * 60, enemy_type="BasicEnemy", spawn_point=(3, 0)) for i in range(5)],
                # 5体のFastEnemyを600,660,720,780,840フレームで出現
                # *[EnemySpawnData(time=600 + i * 60, enemy_type="FastEnemy", spawn_point=(3, 0)) for i in range(5)],
                # 5体のTankEnemyを1200,1260,1320,1380,1440フレームで出現
                # *[EnemySpawnData(time=1200 + i * 60, enemy_type="TankEnemy", spawn_point=(3, 0)) for i in range(5)],
                # 5体のFlyingEnemyを1800,1860,1920,1980,2040フレームで出現
                # *[
                #   FlyingEnemySpawnData(time=1800 + i * 60, spawn_point=(9, 0), landing_point=(13, 6))
                #   for i in range(5)
                # ],
            ]
        ),
        StageWaveData([]),
    ],
)
