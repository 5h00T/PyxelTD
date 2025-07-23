"""
FontRenderer - 任意のフォントでテキスト描画を行うユーティリティクラス
"""

import pyxel


class FontRenderer:
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    """
    フォント名でBDFフォントを管理し、テキスト描画を行うシングルトンユーティリティ。
    """

    _font_instances: dict[str, "FontRenderer"] = {}
    _name_to_path: dict[str, str] = {}

    def __init__(self, font_path: str) -> None:
        self.font_path = font_path
        self.font = pyxel.Font(font_path)

    @classmethod
    def register_font(cls, name: str, font_path: str) -> None:
        """
        フォント名とパスを登録し、インスタンスを生成しておく。
        """
        cls._name_to_path[name] = font_path
        if font_path not in cls._font_instances:
            cls._font_instances[font_path] = cls(font_path)

    @classmethod
    def get_by_name(cls, name: str) -> "FontRenderer":
        """
        フォント名からインスタンスを取得。
        """
        font_path = cls._name_to_path.get(name)
        if not font_path:
            raise ValueError(f"Font name '{name}' is not registered.")
        return cls._font_instances[font_path]

    @classmethod
    def draw_text(cls, x: int, y: int, text: str, color: int = 7, font_name: str = "default") -> None:
        """
        指定フォント名でテキストを描画。
        """
        renderer = cls.get_by_name(font_name)
        pyxel.text(x, y, text, color, renderer.font)

    @classmethod
    def text_width(cls, text: str, font_name: str = "default") -> int:
        """
        指定フォント名でテキスト幅を取得。
        """
        renderer = cls.get_by_name(font_name)
        return renderer.font.text_width(text)
