from enum import Enum

import pygame
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Sprite
from abc import ABC, abstractmethod
from core.settings import TILESIZE

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


class AnimationProperty(UpdateProperty):
    def __init__(self, sprite_prop, columns_count=4, tile_size=TILESIZE, looping=True, running=False, starting_frame=0,
                 current_frame=0):
        self.sprite_prop = sprite_prop
        self.columns_count = columns_count
        self.tile_size = tile_size
        self._frames_count = 4
        self.current_frame = current_frame
        self._starting_frame = starting_frame
        self.looping = looping
        self.running = running
        self.interval = 1
        self.accumulated_time_s = 0

    @property
    def starting_frame(self):
        return self._starting_frame

    @starting_frame.setter
    def starting_frame(self, frame):
        self._starting_frame = frame
        self.set_frame(frame)

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval_s):
        self._interval = interval_s
        self._duration = self.interval * self.frames_count

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration_s):
        self._duration = duration_s
        self._interval = self.duration / self.frames_count

    @property
    def frames_count(self):
        return self._frames_count

    @frames_count.setter
    def frames_count(self, count):
        self._frames_count = count
        self._duration = self.interval * self.frames_count


    def set_frame(self, index):
        self.current_frame = index
        self.sprite_prop.update_clip_rect(self.current_frame)

    def next_frame(self):
        self.current_frame += 1
        if self.looping:
            if self.current_frame >= self.starting_frame + self.frames_count:
                self.current_frame -= self.starting_frame
                self.current_frame %= self.frames_count
                self.current_frame += self.starting_frame
        elif self.current_frame >= self.starting_frame + self.frames_count:
            self.current_frame = self.starting_frame + self.frames_count - 1
            self.running = False
        self.set_frame(self.current_frame)

    def update(self, *args, dt, **kwargs):
        if self.running:
            self.accumulated_time_s += dt
            if self.accumulated_time_s > self.interval:
                self.accumulated_time_s -= self.interval
                self.next_frame()


class MovementAnimationProperty(AnimationProperty):
    keyframes = {
        'up': 0,
        'right': 4,
        'down': 8,
        'left': 12,
    }

    def __init__(self, sprite_prop, moving_prop):
        super().__init__(sprite_prop)
        self.moving_prop = moving_prop
        self.duration = 150 / moving_prop.speed
        self.running = True
        self.looping = True
        self.last_keyframe = MovementAnimationProperty.keyframes['down']

    def select_keyframe(self, dir_x, dir_y):
        if dir_y < 0:
            return self.keyframes['down']
        if dir_y > 0:
            return self.keyframes['up']
        if dir_x < 0:
            return self.keyframes['left']
        if dir_x > 0:
            return self.keyframes['right']
        return None

    def update(self, *args, dt, **kwargs):
        super(MovementAnimationProperty, self).update(*args, dt=dt, **kwargs)
        direction = self.moving_prop.direction
        keyframe = self.select_keyframe(*direction)
        # Debugger.print('Last, key, start', self.last_keyframe, keyframe, self.starting_frame)

        if keyframe is not None:
            if self.last_keyframe != keyframe:
                self.looping = True
                self.running = True
                self.starting_frame = keyframe
            self.last_keyframe = keyframe
        else:
            # stop
            self.looping = False
            self.starting_frame = self.last_keyframe


class SpriteProperty(RenderProperty):
    def __init__(self, image, world, position, dimensions=None, columns_count=4, visible=False, stack_layer=0):
        self.world = world
        self.stack_layer = stack_layer
        self.sprite = Sprite()  # no graoup at start = visible False
        self.sprite.image = image
        if not dimensions:
            dimensions = image.get_width(), image.get_height()
        self.sprite.rect = Rect(position, dimensions)
        self.visible = visible
        self.clip_rect = Rect((0, 0), self.rect.size)
        self._columns_count = columns_count

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

    @property
    def columns_count(self):
        return self._columns_count

    @columns_count.setter
    def columns_count(self, count):
        self._columns_count = count
        self.update_clip_rect(0)

    @visible.setter
    def visible(self, vis):
        self._visible = vis
        if self._visible:
            WorldRenderer.add_visible_object(self)
        else:
            WorldRenderer.remove_visible_object(self)

    def update_clip_rect(self, index):
        self.clip_rect.x = self.rect.w * (index % self._columns_count)
        self.clip_rect.y = self.rect.h * (index // self._columns_count)

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
        self.apply_key(keys)

    def apply_key(self, keys, axis_asnap=True):
        if axis_asnap:
            if keys[pygame.K_w]:
                self.moving_prop.direction = Vector2(0, -1)
            elif keys[pygame.K_s]:
                self.moving_prop.direction = Vector2(0, 1)
            elif keys[pygame.K_a]:
                self.moving_prop.direction = Vector2(-1, 0)
            elif keys[pygame.K_d]:
                self.moving_prop.direction = Vector2(1, 0)
            else:
                self.moving_prop.direction = Vector2(0, 0)
        else:
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
    ANIMATION = AnimationProperty
    MOVEMENT_ANIMATION = MovementAnimationProperty
