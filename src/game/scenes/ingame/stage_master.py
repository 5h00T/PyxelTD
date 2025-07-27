"""
ステージマスターデータ定義
"""

from typing import List


class EnemySpawnData:
    """
    1体のエネミー出現情報
    """

    def __init__(self, time: int, enemy_type: str, path_id: int):
        self.time = time  # 出現フレーム
        self.enemy_type = enemy_type  # "BasicEnemy"など
        self.path_id = path_id  # どのパスを使うか


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

    def __init__(self, map_id: int, paths: List[List[tuple[int, int]]], waves: List[StageWaveData]):
        self.map_id = map_id
        self.paths = paths  # 経路リスト（後からセットも可）
        self.waves = waves


# --- サンプルデータ ---
SAMPLE_STAGE_MASTER = StageMasterData(
    map_id=1,
    paths=[],  # マップ生成後にセットする
    waves=[
        StageWaveData(
            [
                # 5体のBasicEnemyを0,60,120,180,240フレームで出現
                *[EnemySpawnData(time=i * 60, enemy_type="BasicEnemy", path_id=0) for i in range(5)],
                # 3体のFastEnemyを600,660,720フレームで出現
                *[EnemySpawnData(time=600 + i * 60, enemy_type="FastEnemy", path_id=1) for i in range(5)],
                # 2体のTankEnemyを1200,1260フレームで出現
                *[EnemySpawnData(time=1200 + i * 60, enemy_type="TankEnemy", path_id=0) for i in range(5)],
                # 1体のFlyingEnemyを1800フレームで出現
                *[EnemySpawnData(time=1800 + i * 60, enemy_type="FlyingEnemy", path_id=0) for i in range(5)],
            ]
        ),
        StageWaveData(
            [
                # 2nd wave: さらに多様な敵を追加可能
                # EnemySpawnData(time=60, enemy_type="TankEnemy", path_id=0),
                # EnemySpawnData(time=90, enemy_type="FastEnemy", path_id=1),
            ]
        ),
    ],
)
