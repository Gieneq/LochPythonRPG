import pygame

from core.debug import Debugger
from core.utils import distance_squared
from entity.player import Player
from world.worldloader import WorldLoader
from core.renderer import WorldRenderer
from core.settings import COLLISION_RANGE_SQUARED


class World:
    def __init__(self):
        self.obstacle_objects = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.player = Player((580, 390), world=self)
        WorldLoader.load_test_map(self)

    def update(self, dt):
        self.obstacle_objects.update(dt=dt)
        self.entities.update(dt=dt)

    def on_player_move(self):
        WorldRenderer.sort_visibility()

    def get_nearby_obstacles(self, entity):
        potentially_colliding_objects = filter(
            lambda x: distance_squared(x.rect.center, entity.rect.center) < COLLISION_RANGE_SQUARED,
            self.obstacle_objects)
        potentially_colliding_objects = list(filter(lambda x: x is not entity, potentially_colliding_objects))

        for obstacle in potentially_colliding_objects:
            Debugger.rect(obstacle.rect, 'Orange')
            Debugger.rect(obstacle.hitbox, 'Yellow')

        return potentially_colliding_objects
