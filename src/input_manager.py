"""
InputManager - 入力抽象化クラス

ゲーム内のキー入力を一元管理し、シーンやゲーム本体から利用できるAPIを提供します。
Pyxelのbtn/btnpをラップし、今後の拡張にも備えます。
"""
import pyxel  # Pyxel: レトロゲーム開発用Pythonライブラリ。キー入力取得に利用。
from typing import Dict, List

class InputManager:
    """
    ゲーム内のキー入力状態とトリガー（1フレーム押下）を管理するクラス。

    Attributes:
        keys (List[int]): 監視対象のキーコード一覧。
        prev_states (Dict[int, bool]): 前フレームのキー押下状態。
        current_states (Dict[int, bool]): 今フレームのキー押下状態。

    Note:
        Pyxelのbtn/btnpをラップし、今後の拡張やテスト容易性を高める設計。
        無効なキーコードは常にFalseを返します。
    """
    def __init__(self, keys: List[int]) -> None:
        """
        InputManagerの初期化。

        Args:
            keys (List[int]): 監視するキーコード一覧。

        Note:
            初期化時に監視対象キーの状態を全てFalseで初期化します。
        """
        self.keys: List[int] = keys
        # 拡張時はkeysの型・値チェックや例外処理（TypeError, ValueError等）を追加推奨
        # prev_states: 前フレームのキー状態（初期値は全てFalse）
        # current_states: 今フレームのキー状態（初期値は全てFalse）
        # これにより、キーの押下/離し判定が可能となる
        self.prev_states: Dict[int, bool] = {key: False for key in keys}
        self.current_states: Dict[int, bool] = {key: False for key in keys}

    def update(self) -> None:
        """
        毎フレーム呼び出し、監視対象キーの状態を更新します。

        前フレームの状態（prev_states）と今フレームの状態（current_states）を更新。
        """
        # 監視対象キーのみ状態を更新
        # Pyxelのbtn関数をラップし、毎フレーム監視対象キーの状態を更新
        for key in self.keys:
            # 複雑な入力（アナログ・マウス等）対応時は専用メソッド分割を推奨
            # 前フレームの状態を保存
            self.prev_states[key] = self.current_states.get(key, False)
            # 今フレームの状態をPyxelから取得
            self.current_states[key] = pyxel.btn(key)

    def is_pressed(self, key: int) -> bool:
        """
        指定キーが現在押されているか判定します。

        Args:
            key (int): 判定するキーコード。

        Returns:
            bool: 押されていればTrue、無効キーはFalse。

        Note:
            pyxel.btn(key)をラップ。監視対象外キーはFalse。
        """
        # 毎フレームupdateで取得したcurrent_statesを参照。監視対象外キーは常にFalse（エッジケース対応）
        return self.current_states.get(key, False) if key in self.keys else False

    def is_triggered(self, key: int) -> bool:
        """
        指定キーが今フレームで押されたか（トリガー）判定します。

        Args:
            key (int): 判定するキーコード。

        Returns:
            bool: 今フレームで押された場合True、無効キーはFalse。

        Note:
            前フレームで押されていなくて、今フレームで押されている場合True。
            監視対象外キーはFalse。
        """
        # prev_states/current_statesの差分でトリガー判定
        return (
            not self.prev_states.get(key, False)
            and self.current_states.get(key, False)
        ) if key in self.keys else False

    def is_released(self, key: int) -> bool:
        """
        指定キーが今フレームで離されたか判定します。

        Args:
            key (int): 判定するキーコード。

        Returns:
            bool: 今フレームで離された場合True、無効キーはFalse。

        Note:
            前フレームで押されていて、今フレームで押されていない場合True。
            監視対象外キーはFalse。
        """
        # 前フレームで押されていて、今フレームで押されていない場合True
        # 監視対象外キーは常にFalse（エッジケース対応）
        # prev_states/current_statesの差分で離し判定
        return (
            self.prev_states.get(key, False)
            and not self.current_states.get(key, False)
        ) if key in self.keys else False
        
    def get_pressed_keys(self) -> List[int]:
        """
        現在押されている監視対象キー一覧を返します。

        Returns:
            List[int]: 押されているキーコード一覧。

        Note:
            current_statesを参照し、Trueのキーのみ返します。
        """
        # current_statesを参照し、押されている監視対象キーのみ返す
        return [key for key in self.keys if self.current_states.get(key, False)]

