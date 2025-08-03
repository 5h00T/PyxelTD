"""
SceneType - ゲームシーンの種類を定義するEnum。
他モジュールから循環参照なしで利用可能。
"""

from enum import Enum


class SceneType(Enum):
    TITLE = 1
    MENU = 2
    STAGE_SELECT = 3
    IN_GAME = 4
