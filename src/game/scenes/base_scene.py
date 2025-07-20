"""
BaseScene - ゲームシーンの基底クラス
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseScene(ABC):
    """
    全てのゲームシーンの基底クラス。
    各シーンは update() と draw() メソッドを実装する必要がある。
    """

    def __init__(self) -> None:
        """シーンの初期化"""
        pass

    @abstractmethod
    def update(self, game: Any, input_manager: Any) -> None:
        """
        シーンの更新処理。

        Args:
            game (Any): Gameクラスのインスタンス（シーン遷移等で使用）
            input_manager (Any): 入力管理クラス

        Returns:
            None
        """
        pass

    @abstractmethod
    def draw(self, game: Any) -> None:
        """
        シーンの描画処理。

        Args:
            game (Any): Gameクラスのインスタンス
            input_manager (Any): 入力管理クラス

        Returns:
            None
        """
        pass
