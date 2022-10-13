import pygame

from core.debug import Debugger
from entity.entity import Entity


class Tile(Entity):
    def __init__(self, starting_pos, world, visible=True):
        super().__init__(world=world)
        self.image = pygame.image.load('./data/graphics/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=starting_pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.set_visible(visible)
        self.set_collideable(True)

    def update(self, dt, *args, **kwargs):
        super().update(*args, **kwargs)
