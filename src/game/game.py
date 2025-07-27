from .utils.font_renderer import FontRenderer

"""
ゲームループ本体とシーン管理を行うGameクラス。
"""

import pyxel
from .scenes.base_scene import BaseScene
from .scenes.title_scene import TitleScene
from .scenes.menu_scene import MenuScene
from .scenes.in_game_scene import InGameScene
from .scenes.stage_select_scene import StageSelectScene
from .input_manager import InputManager

from .scenes.scene_type import SceneType


class Game:
    """
    ゲーム全体のループとシーン管理を担当するクラス。
    """

    # Windowサイズ
    WINDOW_WIDTH = 160
    WINDOW_HEIGHT = 120

    def __init__(self) -> None:
        pyxel.init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # フォント登録（必要に応じて複数登録可）
        FontRenderer.register_font("default", "../../assets/fonts/misaki_bdf_2021-05-05/misaki_mincho.bdf")
        FontRenderer.register_font("gothic", "../../assets/fonts/misaki_bdf_2021-05-05/misaki_gothic.bdf")
        self.input_manager = InputManager(
            [
                # ESCは終了なので除外
                pyxel.KEY_UP,
                pyxel.KEY_DOWN,
                pyxel.KEY_LEFT,
                pyxel.KEY_RIGHT,
                pyxel.KEY_SPACE,
                pyxel.KEY_RETURN,
                pyxel.KEY_P,
                pyxel.KEY_Q,
                pyxel.KEY_Z,
                pyxel.KEY_X,
                pyxel.KEY_R,
            ]
        )
        self.scenes = {
            SceneType.TITLE: TitleScene,
            SceneType.MENU: MenuScene,
            SceneType.STAGE_SELECT: StageSelectScene,
            SceneType.IN_GAME: InGameScene,
        }
        self.current_scene: BaseScene = self.scenes[SceneType.TITLE]()  # 初期シーンはタイトル画面
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        毎フレーム呼び出し。入力更新→現在のシーンの更新処理。
        """
        self.input_manager.update()
        if self.current_scene:
            self.current_scene.update(self, self.input_manager)

    def draw(self) -> None:
        """
        現在のシーンの描画処理を呼び出す。
        """
        if self.current_scene:
            self.current_scene.draw(self)

    def change_scene(self, new_scene: SceneType) -> None:
        """
        シーンを変更する。

        Args:
            new_scene: 新しいシーンのインスタンス
        """
        self.current_scene = self.scenes[new_scene]()
