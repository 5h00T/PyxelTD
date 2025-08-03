from enum import Enum


class InGameResult(Enum):
    """
    インゲームシーンの結果を表すEnum。
    """

    NONE = 0
    STAGE_SELECT = 1
    RETRY = 2
