"""
FontRenderer - 任意のフォントでテキスト描画を行うユーティリティクラス
"""

import pyxel
from typing import Any


class FontRenderer:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "FontRenderer":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # インスタンス変数の初期化
            cls._instance._font_instances = {}
            cls._instance._name_to_path = {}
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._font_instances: dict[str, pyxel.Font] = {}
            self._name_to_path: dict[str, str] = {}
            self._initialized = True

    @staticmethod
    def get_instance() -> "FontRenderer":
        return FontRenderer()

    def register_font(self, name: str, font_path: str) -> None:
        """
        フォント名とパスを登録し、インスタンスを生成しておく。
        """
        self._name_to_path[name] = font_path
        if font_path not in self._font_instances:
            self._font_instances[font_path] = pyxel.Font(font_path)

    def _get_font(self, name: str) -> pyxel.Font:
        font_path = self._name_to_path.get(name)
        if not font_path:
            raise ValueError(f"Font name '{name}' is not registered.")
        return self._font_instances[font_path]

    def draw_text(self, x: int, y: int, text: str, color: int = 7, font_name: str = "default") -> None:
        """
        指定フォント名でテキストを描画。
        """
        font = self._get_font(font_name)
        pyxel.text(x, y, text, color, font)

    def text_width(self, text: str, font_name: str = "default") -> int:
        """
        指定フォント名でテキスト幅を取得。
        """
        font = self._get_font(font_name)
        return font.text_width(text)
