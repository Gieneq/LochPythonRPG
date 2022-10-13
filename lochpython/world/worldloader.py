from core.settings import *
from entity.tile import Tile

TEST_WORLD_MAP = [
    ['x', 'x', 'x', 'x', 'x', 'x'],
    ['x', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', 'x'],
    ['x', 'x', 'x', 'x', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', 'x', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', 'x', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', 'x'],
    ['x', 'x', 'x', 'x', 'x', 'x'],
]


class WorldLoader:
    @staticmethod
    def load_test_map(world):
        for row_idx, row in enumerate(TEST_WORLD_MAP):
            for col_idx, col in enumerate(row):
                if col == 'x':
                    x = col_idx * TILESIZE
                    y = row_idx * TILESIZE
                    Tile((x, y), world)
