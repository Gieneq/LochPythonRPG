from pygame.math import Vector2
from pygame.sprite import Group

from core.debug import Debugger
from core.utils import distance_squared
from entity.player import Player
from world.worldloader import WorldLoader
from core.renderer import WorldRenderer
from core.settings import COLLISION_RANGE_SQUARED


class Camera(Vector2):
    def __init__(self, focus_point=Vector2(0, 0), inertial=True):
        super().__init__()
        self.xy = focus_point
        self.inertial = inertial
        self.target_pos = Vector2(self)
        self.velocity = Vector2(0, 0)
        self.focused_entity = None
        self.speed = 4.5

    def focus_on_entity(self, entity, refresh=True):
        self.focused_entity = entity
        if refresh:
            self.xy = self.focused_entity.rect.center

    def update_camera(self, dt):
        if self.focused_entity:
            self.target_pos = self.focused_entity.rect.center

        if not self.inertial:
            self.xy = self.target_pos
        else:
            self.xy += dt * self.velocity
            self.velocity = (self.target_pos - self.xy) * self.speed

    def __str__(self):
        return f"Looking at: {self.focused_entity} {self.target_pos}, has pos: {self.xy}, vel: {self.velocity}"


class World:
    def __init__(self):
        self.obstacle_objects = Group()
        self.entities = Group()

        self.player = Player((580, 390), world=self)
        WorldLoader.load_test_map(self)
        self.camera = Camera()
        self.camera.focus_on_entity(self.player)

    def update(self, dt):
        self.obstacle_objects.update(dt=dt)
        self.entities.update(dt=dt)
        self.camera.update_camera(dt=dt)

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
