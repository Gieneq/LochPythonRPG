import pygame

from . import debug
from .settings import *
from .tile import Rock
from .player import Player

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
        for row_idx, row in enumerate(WORLD_MAP):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                if col == 'x':
                    Rock((x,y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)


    def run(self):
        # self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug.text(y=30, msg=f'p:{self.player.direction}')


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width()//2
        self.half_height = self.display_surface.get_height()//2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda s:s.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)