from abc import ABC, abstractmethod


class ISpeedBuff(ABC):
    @abstractmethod
    def get_speed_multiplier(self) -> float:
        """
        バフの速度倍率を取得するメソッド。
        """
        ...


class ITimerBuff(ABC):
    @abstractmethod
    def get_duration(self) -> int:
        """
        バフの持続時間を取得するメソッド。
        """
        ...


class BuffBase(ABC):
    """
    バフのインターフェース。
    すべてのバフはこのインターフェースを実装する必要がある。
    """

    def __init__(self) -> None: ...

    @abstractmethod
    def update(self) -> bool:
        """
        バフの効果を更新するメソッド。
        返り値がTrueの場合、バフは削除される。
        """
        ...

    def is_allow_duplicate(self) -> bool:
        """
        同じクラスのバフを重複して適用できるかどうかを返す。
        デフォルトはFalse。
        """
        return False


class SpeedDownBuff(BuffBase, ISpeedBuff, ITimerBuff):
    """
    敵の移動速度を下げるバフ。
    """

    def __init__(self, duration: int, speed_multiplier: float) -> None:
        super().__init__()
        self.duration = duration
        self.speed_multiplier = speed_multiplier

    def update(self) -> bool:
        """
        バフの効果を更新する。
        持続時間が0以下になったらバフを削除する。
        """
        self.duration -= 1

        return self.duration <= 0

    def get_speed_multiplier(self) -> float:
        """
        バフの速度倍率に加算する値を取得
        """
        return -self.speed_multiplier

    def get_duration(self) -> int:
        """
        バフの持続時間を取得する。
        """
        return self.duration
