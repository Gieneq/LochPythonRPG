import pygame

from core.settings import *
# from entity.tile import Tile
from objects.go import GameObject
from objects.property import Props, SpriteProperty, CollisionProperty, MovingProperty, WSADDriven

TEST_WORLD_MAP = [
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
]


class ImagesLoader:
    instance = None

    def __init__(self):
        self.floor_image = pygame.image.load('./data/graphics/floor.png').convert_alpha()
        self.player = pygame.image.load('./data/graphics/player.png').convert_alpha()
        self.rock = pygame.image.load('./data/graphics/rock.png').convert_alpha()


if not ImagesLoader.instance:
    ImagesLoader.instance = ImagesLoader()
loader = ImagesLoader.instance


class WorldLoader:
    @staticmethod
    def load_test_map(world):
        # todo better but still bad, move out to database
        # image = pygame.image.load('./data/graphics/floor.png').convert_alpha()
        for row_idx, row in enumerate(TEST_WORLD_MAP):
            for col_idx, col in enumerate(row):
                if col == 'x':
                    x = col_idx * TILESIZE
                    y = row_idx * TILESIZE

                    floor_tile = GameObject().with_sprite(
                        SpriteProperty(loader.rock, world, (x, y), dimensions=(TILESIZE, TILESIZE), visible=True))
                    world.floor.append(floor_tile)
                    limit_block = GameObject().with_collision(
                        CollisionProperty(floor_tile.properties[Props.SPRITE].rect, world))
                    world.limit_blocks.append(limit_block)


        player_sprite = SpriteProperty(loader.player, world, (580, 390), visible=True)
        player_coll = CollisionProperty(player_sprite.rect, world)
        player_moving = MovingProperty(player_coll, world)
        player_wsad = WSADDriven(player_moving)

        player = GameObject().with_sprite(player_sprite).with_moving(player_moving).with_wsad(player_wsad).with_collision(player_coll)
        world.entities.append(player)
        world.player = player
