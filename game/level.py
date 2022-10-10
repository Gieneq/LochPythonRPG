import pygame
from .settings import *
from .tile import Rock
from .player import Player

class Level:
    def __init__(self):

        # get display furface
        self.display_surface = pygame.display.get_surface()

        # sprites groups setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_idx, row in enumerate(WORLD_MAP):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                if col == 'x':
                    Rock((x,y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    Player((x,y), [self.visible_sprites])


    def run(self):
        self.visible_sprites.draw(self.display_surface)
