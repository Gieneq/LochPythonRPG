import pygame
from pygame.rect import Rect

from .settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = surface  # pygame.image.load('./graphics/rock.png').convert_alpha()
        self.sprite_type = sprite_type


        if self.sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-TILESIZE))
            self.hitbox = self.rect.copy()
            self.hitbox.y += TILESIZE
            self.hitbox.h -= TILESIZE
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.copy()

        self.hitbox = self.hitbox.inflate(0, -10)
