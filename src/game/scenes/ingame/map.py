"""
Map - シンプルなマップタイル管理クラス
各タイルは8x8px、種別ごとに描画方法を分岐
"""

from typing import List

from typing import Optional

# タイル種別定数
TILE_PATH = 0  # 敵の道（灰色）
TILE_PLACEABLE = 1  # ユニット配置可能（白）
TILE_BLOCKED = 2  # ユニット配置不可（バツ印）
TILE_GOAL = 3  # ゴール地点（緑）


class Map:

    def get_tile(self, x: int, y: int) -> int:
        """
        Returns the tile type at (x, y). Out of bounds returns TILE_BLOCKED (2).
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y][x]
        return 2

    def get_all_paths_from_entrances_to_goal(self) -> list[list[tuple[int, int]]]:
        """
        マップ端のTILE_PATH=0を入口とし、各入口からゴールまでの経路を抽出。
        Returns:
            list[list[tuple[int, int]]]: 各入口からゴールまでの経路リスト
        """
        height = self.height
        width = self.width
        # 入口（画面外に隣接するTILE_PATH）を左端・上端・右端・下端から探す
        entrances = []
        for y in range(height):
            if self.data[y][0] == TILE_PATH:
                entrances.append((0, y))
            if self.data[y][width - 1] == TILE_PATH:
                entrances.append((width - 1, y))
        for x in range(width):
            if self.data[0][x] == TILE_PATH:
                entrances.append((x, 0))
            if self.data[height - 1][x] == TILE_PATH:
                entrances.append((x, height - 1))
        # ゴール（TILE_GOAL=3）を探す
        goal = None
        for y in range(height):
            for x in range(width):
                if self.data[y][x] == TILE_GOAL:
                    goal = (x, y)
                    break
            if goal:
                break
        if not goal:
            return []
        # 各入口からゴールまでの経路を幅優先探索で抽出
        from collections import deque
        from typing import Optional, Tuple

        paths = []
        for start in entrances:
            visited = [[False] * width for _ in range(height)]
            prev: list[list[Optional[Tuple[int, int]]]] = [[None for _ in range(width)] for _ in range(height)]
            queue: deque[Tuple[int, int]] = deque()
            sx, sy = start
            queue.append((sx, sy))
            visited[sy][sx] = True
            found = False
            while queue:
                x, y = queue.popleft()
                if (x, y) == goal:
                    found = True
                    break
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if not visited[ny][nx] and (self.data[ny][nx] == TILE_PATH or self.data[ny][nx] == TILE_GOAL):
                            visited[ny][nx] = True
                            prev[ny][nx] = (x, y)
                            queue.append((nx, ny))
            # ゴールまでの経路を復元
            if found:
                path = []
                x, y = goal
                while (x, y) != start:
                    path.append((x, y))
                    if prev[y][x] is None:
                        break
                    # 安全にアンパック
                    next_pos = prev[y][x]
                    if next_pos is None:
                        break
                    x, y = next_pos
                path.append(start)
                path.reverse()
                paths.append(path)
        return paths

    def get_path_from_entrance_to_goal(self) -> list[tuple[int, int]]:
        """
        マップデータから入口（画面外）→道（TILE_PATH=0）→ゴール（TILE_GOAL=3）までの経路を抽出。
        Returns:
            list[tuple[int, int]]: 経路となるタイル座標リスト
        """
        TILE_PATH = 0
        TILE_GOAL = 3
        height = self.height
        width = self.width
        # 入口（画面外に隣接するTILE_PATH）を左端・上端・右端・下端から探す
        entrances = []
        for y in range(height):
            if self.data[y][0] == TILE_PATH:
                entrances.append((0, y))
            if self.data[y][width - 1] == TILE_PATH:
                entrances.append((width - 1, y))
        for x in range(width):
            if self.data[0][x] == TILE_PATH:
                entrances.append((x, 0))
            if self.data[height - 1][x] == TILE_PATH:
                entrances.append((x, height - 1))
        if not entrances:
            return []
        start = entrances[0]  # 最初の入口を採用
        # ゴール（TILE_GOAL=3）を探す
        goal = None
        for y in range(height):
            for x in range(width):
                if self.data[y][x] == TILE_GOAL:
                    goal = (x, y)
                    break
            if goal:
                break
        if not goal:
            return []
        # 経路探索（幅優先探索でTILE_PATHとTILE_GOALを辿る）
        from collections import deque
        from typing import Optional, Tuple

        visited = [[False] * width for _ in range(height)]
        prev: list[list[Optional[Tuple[int, int]]]] = [[None for _ in range(width)] for _ in range(height)]
        queue: deque[Tuple[int, int]] = deque()
        sx, sy = start
        queue.append((sx, sy))
        visited[sy][sx] = True
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if not visited[ny][nx] and (self.data[ny][nx] == TILE_PATH or self.data[ny][nx] == TILE_GOAL):
                        visited[ny][nx] = True
                        prev[ny][nx] = (x, y)
                        queue.append((nx, ny))
        # ゴールまでの経路を復元
        path = []
        x, y = goal
        while (x, y) != start:
            path.append((x, y))
            if prev[y][x] is None:
                # 経路が途切れている場合
                return []
            # 安全にアンパック
            next_pos = prev[y][x]
            if next_pos is None:
                return []
            x, y = next_pos
        path.append(start)
        path.reverse()
        return path

    """
    マップタイル管理クラス。
    2次元リストでマップデータを保持。
    """

    def __init__(self, width: int, height: int) -> None:
        """
        マップ初期化。仮ステージデータ生成。
        Args:
            width (int): マップ横タイル数（仮）
            height (int): マップ縦タイル数（仮）
        Note:
            実際のマップサイズは生成された2次元配列のサイズに合わせて自動設定されます。
        """
        self.data: List[List[int]] = self.generate_sample_stage(width, height)
        # 実際のマップサイズを配列から取得
        self.height = len(self.data)
        self.width = len(self.data[0]) if self.data else 0

    @staticmethod
    def generate_sample_stage(width: int, height: int) -> List[List[int]]:
        """
        仮ステージ用のマップデータ生成。
        - 0: 敵通行可能
        - 1: ユニット配置可能
        - 2: ユニット配置不可
        """
        data = [
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 2, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 2, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        ]

        return data

    def draw(
        self, camera_x: int = 0, camera_y: int = 0, view_width: Optional[int] = None, view_height: Optional[int] = None
    ) -> None:
        """
        カメラ範囲のみマップを描画。
        Args:
            camera_x (int): カメラ左上タイルX
            camera_y (int): カメラ左上タイルY
            view_width (int): 画面表示タイル数X
            view_height (int): 画面表示タイル数Y
        """
        import pyxel
        from .constants import TILE_SIZE, VIEW_TILE_WIDTH, VIEW_TILE_HEIGHT

        view_width = view_width if view_width is not None else VIEW_TILE_WIDTH
        view_height = view_height if view_height is not None else VIEW_TILE_HEIGHT
        for y in range(camera_y, min(camera_y + view_height, self.height)):
            for x in range(camera_x, min(camera_x + view_width, self.width)):
                tile = self.data[y][x]
                px = (x - camera_x) * TILE_SIZE
                py = (y - camera_y) * TILE_SIZE
                if tile == TILE_PATH:
                    pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 5)  # 灰色
                elif tile == TILE_PLACEABLE:
                    pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 7)  # 白
                elif tile == TILE_BLOCKED:
                    pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 7)  # 白地
                    pyxel.line(px, py, px + TILE_SIZE - 1, py + TILE_SIZE - 1, 8)  # バツ印
                    pyxel.line(px + TILE_SIZE - 1, py, px, py + TILE_SIZE - 1, 8)
                elif tile == TILE_GOAL:
                    # --- 拠点（城）グラフィック ---
                    # 土台
                    pyxel.rect(px, py, TILE_SIZE, TILE_SIZE, 13)  # 薄グレー
                    # 城壁
                    pyxel.rectb(px, py, TILE_SIZE, TILE_SIZE, 1)  # 黒枠
                    # 中央塔
                    tower_w = TILE_SIZE // 2
                    tower_h = TILE_SIZE // 2
                    tower_x = px + (TILE_SIZE - tower_w) // 2
                    tower_y = py + (TILE_SIZE - tower_h) // 2
                    pyxel.rect(tower_x, tower_y, tower_w, tower_h, 7)  # 白
                    # 旗
                    flag_x = tower_x + tower_w // 2
                    flag_y = tower_y
                    pyxel.line(flag_x, flag_y, flag_x, flag_y - 3, 8)  # ポール
                    pyxel.rect(flag_x, flag_y - 3, 3, 2, 8)  # 赤旗
