import random

import pygame

from core.utils import import_csv_layout, import_folder
from core.debug import DebugWriter
from core.settings import *
from .tile import Tile
from entity.player import Player


class Level:
    def __init__(self):

        # get display furface
        self.display_surface = pygame.display.get_surface()

        # sprites groups setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # map setup
        self.create_map()

    def create_map(self):
        # layout = {
        #     'boundary': import_csv_layout('../../data/map/map_FloorBlocks.csv'),
        #     'grass': import_csv_layout('../../data/map/map_Grass.csv'),
        #     'object': import_csv_layout('../../data/map/map_LargeObjects.csv'),
        # }
        #
        # graphics = {
        #     'grass': import_folder('../../data/graphics/grass'),
        #     'object': import_folder('../../data/graphics/objects'),
        # }
        #
        # for style, layout in layout.items():
        #     for row_idx, row in enumerate(layout):
        #         for col_idx, col in enumerate(row):
        #             if col != '-1':
        #                 x = col_idx * TILESIZE
        #                 y = row_idx * TILESIZE
        #                 if style == 'boundary':
        #                     Tile((x, y), [self.obstacle_sprites], sprite_type='invisible')
        #                 if style == 'grass':
        #                     grass_surface = random.choice(graphics['grass'])
        #                     Tile((x, y), [self.visible_sprites, self.obstacle_sprites], sprite_type='grass', surface=grass_surface)
        #                 if style == 'object':
        #                     object_surf = graphics['object'][int(col)]
        #                     Tile((x, y), [self.visible_sprites, self.obstacle_sprites], sprite_type='object', surface=object_surf)

        self.player = Player((757, 1242), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        DebugWriter.print(f'p_dir:{self.player.direction}')
        DebugWriter.print(f'p_center:{self.player.rect.center}')


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load('./data/graphics/tilemap/ground.png')
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, offset_position)

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
