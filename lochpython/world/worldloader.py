import random

import pygame

from core.settings import *
# from entity.tile import Tile
from objects.go import GameObject
from objects.property import Props, SpriteProperty, CollisionProperty, MovingProperty, WSADDriven, AnimationProperty, \
    MovementAnimationProperty

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
        # todo add meta data like grid size, tile width
        self.floor_image = pygame.image.load('./data/graphics/floor.png').convert_alpha()
        self.water_image = pygame.image.load('./data/graphics/water.png').convert_alpha()
        # self.water_image = pygame.transform.scale2x(self.water_image)
        # self.water_image = pygame.transform.scale2x(self.water_image)
        self.floor_borders = pygame.image.load('./data/graphics/borders.png').convert_alpha()
        self.objects = pygame.image.load('./data/graphics/objects.png').convert_alpha()
        self.player = pygame.image.load('./data/graphics/player_test.png').convert_alpha()
        self.rock = pygame.image.load('./data/graphics/rock.png').convert_alpha()


if not ImagesLoader.instance:
    ImagesLoader.instance = ImagesLoader()
loader = ImagesLoader.instance


class WorldLoader:
    FLOOR_DATA = {
        'grid': 8,
        'ids': {
            0: 'water',
            1: 'grass',
            2: 'dirt',
            3: 'sand',
            4: 'cobble',
            5: 'planks',
        }
    }

    @staticmethod
    def load_csv_map(path):
        with open(path, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]

    # def import_folder(path):
    #     surfaces_list = []
    #     for _, __, img_filenames in walk(path):
    #         for img_filename in img_filenames:
    #             img_path = path + '/' + img_filename
    #             img_surf = pygame.image.load(img_path).convert_alpha()
    #             surfaces_list.append(img_surf)
    #     return surfaces_list

    @staticmethod
    def load_test_map(world):
        # todo better but still bad, move out to database
        # image = pygame.image.load('./data/graphics/floor.png').convert_alpha()

        floor_data = WorldLoader.load_csv_map('./data/map/floor.csv')
        details_data = WorldLoader.load_csv_map('./data/map/borders.csv')
        limit_data = WorldLoader.load_csv_map('./data/map/limit.csv')
        objects_data = WorldLoader.load_csv_map('./data/map/limit.csv')

        # floor
        for row_idx, row in enumerate(floor_data):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                dimension = (TILESIZE, TILESIZE)
                idx = int(col)
                floor_tile = GameObject()
                # todo indicate tile is animated, some need for metadata 😒
                if idx == 0:
                    image = loader.water_image
                    col_count = 2
                else:
                    image = loader.floor_image
                    col_count = 1
                sprite_prop = SpriteProperty(image, world, (x, y), dimensions=dimension, visible=True, columns_count=col_count)
                floor_tile.with_sprite(sprite_prop)

                if idx == 0:
                    anim_prop = AnimationProperty(sprite_prop, running=True, looping=True)
                    anim_prop.columns_count = 2
                    floor_tile.with_animation(anim_prop)
                else:
                    # todo add columns cout to sprite
                    sprite_prop.clip_rect.x = (idx % 8) * TILESIZE
                    sprite_prop.clip_rect.y = (idx // 8) * TILESIZE

                world.floor.append(floor_tile)

                # trees
                if idx == 1:
                    if random.random() < 0.23:
                        idx_tree = random.randint(0,2)
                        object_tile = GameObject()
                        sprite_prop = SpriteProperty(loader.objects, world, (x, y), dimensions=dimension, visible=True, stack_layer=2)
                        sprite_prop.clip_rect.x = (idx_tree % 8) * TILESIZE
                        sprite_prop.clip_rect.y = (idx_tree // 8) * TILESIZE
                        coll_prop = CollisionProperty(sprite_prop.rect, world)
                        object_tile.with_sprite(sprite_prop).with_collision(coll_prop)
                        world.entities.append(object_tile)



        # details
        for row_idx, row in enumerate(details_data):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                dimension = (TILESIZE, TILESIZE)
                idx = int(col)
                if idx == -1:
                    continue
                detail_tile = GameObject()
                sprite_prop = SpriteProperty(loader.floor_borders, world, (x, y), dimensions=dimension, visible=True, stack_layer=1)
                sprite_prop.clip_rect.x = (idx % 8) * TILESIZE
                sprite_prop.clip_rect.y = (idx // 8) * TILESIZE
                detail_tile.with_sprite(sprite_prop)
                world.floor_details.append(detail_tile)

        #objects
        for row_idx, row in enumerate(objects_data):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                dimension = (TILESIZE, TILESIZE)
                idx = int(col)
                if idx > -1 and idx != 3:
                    object_tile = GameObject()
                    sprite_prop = SpriteProperty(loader.objects, world, (x, y), dimensions=dimension, visible=True, stack_layer=2)
                    sprite_prop.clip_rect.x = (idx % 8) * TILESIZE
                    sprite_prop.clip_rect.y = (idx // 8) * TILESIZE
                    object_tile.with_sprite(sprite_prop)
                    world.entities.append(object_tile)


        # limits
        for row_idx, row in enumerate(limit_data):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                if col != '-1':
                    # floor_tile.properties[Props.SPRITE].rect
                    limit_rect = pygame.Rect((x, y), (TILESIZE, TILESIZE))
                    limit_block = GameObject().with_collision(CollisionProperty(limit_rect, world))
                    world.limit_blocks.append(limit_block)

        player_sprite = SpriteProperty(loader.player, world, (590, 440), (20, 40), visible=True, stack_layer=2)
        player_coll = CollisionProperty(player_sprite.rect, world)
        player_moving = MovingProperty(player_coll, world)
        player_wsad = WSADDriven(player_moving)
        anim_prop = MovementAnimationProperty(player_sprite, player_moving)
        # anim_prop.next_frame()
        player = GameObject().with_sprite(player_sprite).with_moving(player_moving).with_wsad(
            player_wsad).with_collision(player_coll).with_animation(anim_prop)
        world.entities.append(player)
        world.player = player
