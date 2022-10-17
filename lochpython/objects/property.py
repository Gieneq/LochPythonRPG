from enum import Enum

import pygame
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Sprite
from abc import ABC, abstractmethod

from core.debug import Debugger
from core.renderer import WorldRenderer


class InputProperty(ABC):
    @abstractmethod
    def input(self, *args, **kwargs):
        print('Input should be overwritten', args, kwargs)


class UpdateProperty:
    @abstractmethod
    def update(self, *args, **kwargs):
        print('Update should be overwritten', args, kwargs)


class RenderProperty:
    @abstractmethod
    def render(self, *args, **kwargs):
        print('Render should be overwritten', args, kwargs)


class SpriteProperty(RenderProperty):
    def __init__(self, image, world, position, dimensions=None, visible=False):
        self.world = world
        self.sprite = Sprite()  # no graoup at start = visible False
        self.sprite.image = image
        if not dimensions:
            dimensions = image.get_width(), image.get_height()
        self.sprite.rect = Rect(position, dimensions)
        self.visible = visible

        self.clip_rect = Rect((0, 0), self.rect.size)

    def __del__(self):
        self.visible = False

    @property
    def rect(self):
        return self.sprite.rect

    @property
    def image(self):
        return self.sprite.image

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, vis):
        self._visible = vis
        if self._visible:
            WorldRenderer.visible_objects.append(self)
        elif self in WorldRenderer.visible_objects:
            WorldRenderer.visible_objects.remove(self)

    def render(self, *args, **kwargs):
        if self.visible:
            Debugger.rect(self.sprite.rect, 'Red')
            self.sprite.update(*args, **kwargs)


class CollisionProperty(UpdateProperty, RenderProperty):
    """This property doesn't mean object checks collison with other objects.
    Can stand still, only moving objects activate collision check"""
    INFLATION = -24

    def __init__(self, parent_rect, world, active=True):
        self.parent_rect = parent_rect
        self.hitbox = None
        self.world = world
        self.active = active
        self.update_hitbox()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active_flag):
        self._active = active_flag
        if self.active:
            self.world.colliding_objects.append(self)
        elif self in self.world.colliding_objects:
            self.world.colliding_objects.remove(self)

    def update_hitbox(self):
        if self.active:
            self.hitbox = Rect(self.parent_rect).inflate(0, CollisionProperty.INFLATION)

    def update(self, *args, **kwargs):
        if self.active:
            self.update_hitbox()

    def render(self, *args, **kwargs):
        if self.active:
            Debugger.rect(self.hitbox, 'Blue')


class MovingProperty(UpdateProperty):
    def __init__(self, collision_prop, world, ignore_collisions=False):
        self.speed = 300
        self.world = world
        self.collision_prop = collision_prop
        self.direction = Vector2(0, 0)
        self.ignore_collisions = ignore_collisions
        self.obstacles_hit = []

    def eval_collision(self, translation, obstacles):
        from_point = Vector2(self.collision_prop.hitbox.topleft)
        # todo capture translation and move source rect of hitbox
        o_encountered_x = self.eval_collision_x(translation, obstacles)
        o_encountered_y = self.eval_collision_y(translation, obstacles)
        to_point = Vector2(self.collision_prop.hitbox.topleft)
        return list(set(o_encountered_x + o_encountered_y)), to_point - from_point

    def eval_collision_x(self, translation, obstacles):
        obstacles_encountered = []
        self.collision_prop.hitbox.x += translation[0]
        for obstacle in obstacles:
            if obstacle.hitbox.colliderect(self.collision_prop.hitbox):
                obstacles_encountered.append(obstacle)
                if translation[0] > 0:
                    self.collision_prop.hitbox.right = obstacle.hitbox.left
                if translation[0] < 0:
                    self.collision_prop.hitbox.left = obstacle.hitbox.right
        return obstacles_encountered

    def eval_collision_y(self, translation, obstacles):
        obstacles_encountered = []
        self.collision_prop.hitbox.y += translation[1]
        for obstacle in obstacles:
            if obstacle.hitbox.colliderect(self.collision_prop.hitbox):
                obstacles_encountered.append(obstacle)
                if translation[1] > 0:
                    self.collision_prop.hitbox.bottom = obstacle.hitbox.top
                if translation[1] < 0:
                    self.collision_prop.hitbox.top = obstacle.hitbox.bottom
        return obstacles_encountered

    def update(self, *args, dt, **kwargs):
        direction = self.direction.copy()  # maybe not necesery
        if direction.magnitude() != 0:
            direction = direction.normalize()

            obstacles = self.world.get_nearby_obstacles(self.collision_prop)
            Debugger.print('Potential obstacles count', len(obstacles))
            for obstacle in obstacles:
                Debugger.rect(obstacle.hitbox, 'Yellow', 3)

            translation = direction * self.speed * dt
            self.obstacles_hit, translation = self.eval_collision(translation, obstacles)

            self.collision_prop.parent_rect.x += translation[0]
            self.collision_prop.parent_rect.y += translation[1]

            for obstacle in self.obstacles_hit:
                Debugger.rect(obstacle.hitbox, 'Yellow', 5)

            if translation.magnitude() != 0:
                self.world.on_player_move()

    def __str__(self):
        return f"Moving dir: {self.direction}, r: {self.collision_prop.parent_rect}"


class WSADDriven(InputProperty, UpdateProperty):

    def __init__(self, moving_prop):
        self.moving_prop = moving_prop

    def input(self, *args, **kwargs):

        keys = pygame.key.get_pressed()
        # movement
        if keys[pygame.K_w]:
            self.moving_prop.direction.y = -1
        elif keys[pygame.K_s]:
            self.moving_prop.direction.y = 1
        else:
            self.moving_prop.direction.y = 0

        if keys[pygame.K_a]:
            self.moving_prop.direction.x = -1
        elif keys[pygame.K_d]:
            self.moving_prop.direction.x = 1
        else:
            self.moving_prop.direction.x = 0

    def update(self, *args, **kwargs):
        Debugger.print(f"WSAD_driven_rect: {self.moving_prop}")


class Props(Enum):
    SPRITE = SpriteProperty
    COLLISION = CollisionProperty
    WSAD_DRIVEN = WSADDriven
    MOVING = MovingProperty
