# シーン管理システム (Scene Management System)

このドキュメントでは、PyxelTDのシーン管理システムについて説明します。

## 概要

ゲームの各画面（タイトル、メニュー、ステージ選択、インゲーム）をシーンとして管理するためのシステムです。

## アーキテクチャ

### BaseScene（基底クラス）
- `src/scenes/base_scene.py`
- 全シーンの基底となる抽象クラス
- `update(game)` と `draw(game)` メソッドを定義

### 具体的なシーンクラス

1. **TitleScene** (`src/scenes/title_scene.py`)
   - ゲームのタイトル画面
   - SPACEキーでメニューに遷移

2. **MenuScene** (`src/scenes/menu_scene.py`)
   - メインメニュー画面
   - 上下キーで選択、SPACEキーで決定
   - Start Game、Settings、Exitの選択肢

3. **StageSelectScene** (`src/scenes/stage_select_scene.py`)
   - ステージ選択画面
   - 4つのステージから選択可能
   - ESCキーでメニューに戻る

4. **InGameScene** (`src/scenes/in_game_scene.py`)
   - ゲームプレイ画面
   - ポーズ機能付き
   - ESCキーでポーズ/メニューに戻る

### Gameクラス
- `src/game.py`
- シーン管理の中心となるクラス
- `current_scene` で現在のシーンを管理
- `change_scene(new_scene)` でシーン遷移

## 使用方法

### シーンの作成
```python
from scenes.base_scene import BaseScene

class MyScene(BaseScene):
    def update(self, game):
        # 更新ロジック
        pass
    
    def draw(self, game):
        # 描画ロジック
        pass
```

### シーン遷移
```python
from scenes.menu_scene import MenuScene

# Gameクラス内またはシーン内で
game.change_scene(MenuScene())
```

## テスト

システムの動作確認には以下のスクリプトを使用：

- `test_scene_structure.py` - 構造の正当性をテスト
- `demo_scene_system.py` - シーン遷移のデモンストレーション

```bash
python test_scene_structure.py
python demo_scene_system.py
```

## 拡張方法

新しいシーンを追加する場合：

1. `src/scenes/` に新しいシーンファイルを作成
2. `BaseScene` を継承し、`update()` と `draw()` を実装
3. `src/scenes/__init__.py` にインポートを追加
4. 他のシーンから遷移できるよう `change_scene()` を呼び出し

このシステムにより、各画面の処理が分離され、保守性・拡張性が向上します。