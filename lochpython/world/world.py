import pygame

from entity.player import Player
from world.worldloader import WorldLoader
from core.renderer import WorldRenderer

class World:
    def __init__(self):
        self.obstacle_objects = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.player = Player((80, 90), world=self)
        WorldLoader.load_test_map(self)

    def update(self, dt):
        self.entities.update(dt=dt)

    def on_player_move(self):
        WorldRenderer.sort_visibility()


