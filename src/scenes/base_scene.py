"""
BaseScene - ゲームシーンの基底クラス
"""
from abc import ABC, abstractmethod


class BaseScene(ABC):
    """
    全てのゲームシーンの基底クラス。
    各シーンは update() と draw() メソッドを実装する必要がある。
    """
    
    def __init__(self):
        """シーンの初期化"""
        pass
    
    @abstractmethod
    def update(self, game):
        """
        シーンの更新処理。
        
        Args:
            game: Gameクラスのインスタンス（シーン遷移等で使用）
        """
        pass
    
    @abstractmethod
    def draw(self, game):
        """
        シーンの描画処理。
        
        Args:
            game: Gameクラスのインスタンス
        """
        pass