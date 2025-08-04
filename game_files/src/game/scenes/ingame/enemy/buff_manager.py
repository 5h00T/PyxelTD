from .buff import BuffBase, ISpeedBuff


class BuffManager:
    """
    敵ユニットのバフ（強化効果）を管理するクラス。
    """

    def __init__(self) -> None:
        self.buffs: list[BuffBase] = []

    def add_buff(self, buff: BuffBase) -> None:
        """
        バフを追加する。
        """
        if not buff.is_allow_duplicate():
            # 既に同じタイプのバフがある場合は追加しない
            for existing_buff in self.buffs:
                if isinstance(existing_buff, type(buff)):
                    return
        self.buffs.append(buff)

    def update(self) -> None:
        """
        バフの効果を更新する。
        """
        new_buffs = []
        for buff in self.buffs:
            if not buff.update():
                new_buffs.append(buff)
        self.buffs = new_buffs

    def get_speed_multiplier(self) -> float:
        """
        指定した敵ユニットの速度倍率を取得。
        バフが適用されていない場合は1.0を返す。
        """
        speed_multiplier = 1.0
        for buff in self.buffs:
            if isinstance(buff, ISpeedBuff):
                speed_multiplier += buff.get_speed_multiplier()
        return speed_multiplier
