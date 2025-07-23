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
                EnemySpawnData(time=60, enemy_type="BasicEnemy", path_id=0),
                EnemySpawnData(time=120, enemy_type="FastEnemy", path_id=0),
                EnemySpawnData(time=180, enemy_type="TankEnemy", path_id=0),
                EnemySpawnData(time=240, enemy_type="BasicEnemy", path_id=0),
                EnemySpawnData(time=300, enemy_type="FastEnemy", path_id=0),
                EnemySpawnData(time=360, enemy_type="TankEnemy", path_id=0),
                EnemySpawnData(time=420, enemy_type="BasicEnemy", path_id=0),
                EnemySpawnData(time=480, enemy_type="FastEnemy", path_id=0),
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
