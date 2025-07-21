# enum
from enum import Enum


class StateResult(Enum):
    """
    ゲームシーンの結果を表すEnum。
    """

    NONE = 0
    STAGE_SELECT = 1
    RETRY = 2
