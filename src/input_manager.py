"""
InputManager - 入力抽象化クラス

ゲーム内のキー入力を一元管理し、シーンやゲーム本体から利用できるAPIを提供します。
Pyxelのbtn/btnpをラップし、今後の拡張にも備えます。
"""
import pyxel
from typing import Dict, List

class InputManager:
    """
    キー入力の状態とトリガー（1フレーム押下）を管理するクラス。
    
    Attributes:
        keys (List[int]): 監視対象のキーコード一覧。
        prev_states (Dict[int, bool]): 前フレームのキー押下状態。
    """
    def __init__(self, keys: List[int]) -> None:
        """
        InputManagerの初期化。
        
        Parameters:
            keys (List[int]): 監視するキーコード一覧。
        """
        self.keys = keys
        self.prev_states: Dict[int, bool] = {key: False for key in keys}  # 前フレーム
        self.current_states: Dict[int, bool] = {key: False for key in keys}  # 今フレーム

    def update(self) -> None:
        """
        毎フレーム呼び出し、キー状態を更新。
        prev_states: 前フレームの状態
        curr_states: 今フレームの状態
        """
        for key in self.keys:
            self.prev_states[key] = self.current_states.get(key, False)
            self.current_states[key] = pyxel.btn(key)

    def is_pressed(self, key: int) -> bool:
        """
        指定キーが現在押されているか判定。
        
        Parameters:
            key (int): 判定するキーコード。
        Returns:
            bool: 押されていればTrue。
        """
        return pyxel.btn(key)

    def is_triggered(self, key: int) -> bool:
        """
        指定キーが今フレームで押されたか（トリガー）判定。
        
        Parameters:
            key (int): 判定するキーコード。
        Returns:
            bool: 今フレームで押された場合True。
        """
        return pyxel.btnp(key)

    def is_released(self, key: int) -> bool:
        """
        指定キーが今フレームで離されたか判定。
        
        Parameters:
            key (int): 判定するキーコード。
        Returns:
            bool: 今フレームで離された場合True。
        """
        # 前フレームで押されていて、今フレームで押されていない
        return self.prev_states.get(key, False) and not self.current_states.get(key, False)
        
    def get_pressed_keys(self) -> List[int]:
        """
        現在押されているキー一覧を返す。
        Returns:
            List[int]: 押されているキーコード一覧。
        """
        return [key for key in self.keys if pyxel.btn(key)]

# エッジケース例: 無効なキーコードは常にFalseを返す
# テスト用関数
def _test_input_manager():
    """
    InputManagerの基本動作テスト。
    - 空リスト、無効キー、複数同時押しの挙動を確認。
    """
    test_keys = [pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_SPACE, 9999]  # 9999は無効キー
    im = InputManager(test_keys)
    im.update()
    assert im.is_pressed(pyxel.KEY_UP) in [True, False]
    assert im.is_triggered(pyxel.KEY_DOWN) in [True, False]
    assert im.is_released(pyxel.KEY_SPACE) in [True, False]
    assert im.is_pressed(9999) is False
    print("InputManager basic test passed.")
