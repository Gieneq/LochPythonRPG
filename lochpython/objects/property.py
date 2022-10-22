from enum import Enum, auto

import pygame
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Sprite
from abc import ABC, abstractmethod
from core.settings import TILESIZE, DEBUG_VISIBLE_OBJECTS, DEBUG_COLLISION_BLOCKS

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


class AnimationPlayer:
    players_register = []

    def __init__(self, frames_count, duration=1, active=True, handlers=None):
        self.frames_count = frames_count
        self.interval = duration / self.frames_count
        self.active = active
        self._accumulated_time_s = 0
        self.handlers = handlers if handlers else []
        # todo add handlers checking if function
        AnimationPlayer.players_register.append(self)

    @property
    def duration(self):
        return self.interval * self.frames_count

    @duration.setter
    def duration(self, duration_s):
        self.interval = duration_s / self.frames_count

    def __del__(self):
        if self in AnimationPlayer.players_register:
            AnimationPlayer.players_register.remove(self)

    def update(self, *args, dt, **kwargs):
        if self.active and self.handlers:
            self._accumulated_time_s += dt
            if self._accumulated_time_s > self.interval:
                self._accumulated_time_s -= self.interval
                for handler in self.handlers:
                    handler()

    @classmethod
    @property
    def total_players(cls):
        return len(cls.players_register)


class AnimationProperty(UpdateProperty):

    def __init__(self, sprite_prop, looping=True, active=False, starting_frame=0, frames_count=1):
        self.sprite_prop = sprite_prop
        self.frames_count = frames_count
        self.starting_frame = starting_frame
        self.looping = looping
        self.active = active
        self.own_player = None #todo default animation player?

    def attach_own_player(self, player):
        self.own_player = player
        player.handlers.append(self.next_frame)

    @property
    def starting_frame(self):
        return self._starting_frame

    @starting_frame.setter
    def starting_frame(self, frame):
        self._starting_frame = frame
        # self.current_frame = frame #todo consider

    @property
    def current_frame(self):
        return self.sprite_prop.image_index

    @current_frame.setter
    def current_frame(self, frame):
        self.sprite_prop.image_index = frame

    def next_frame(self):
        next_index = self.current_frame + 1
        if next_index >= self.starting_frame + self.frames_count:
            if self.looping:
                next_index = ((next_index - self.starting_frame) % self.frames_count) + self.starting_frame
            else:
                next_index = self.starting_frame + self.frames_count - 1

        self.current_frame = next_index

    def update(self, *args, dt, **kwargs):
        if self.active and self.own_player:
            self.own_player.update(*args, dt=dt, **kwargs)


class MovementAnimationProperty(AnimationProperty):
    class EntityState(Enum):
        IDLE = 0
        MOVING = 1

        @classmethod
        def get_state(cls, moving_prop):
            return cls.MOVING if moving_prop.direction.magnitude() != 0 else cls.IDLE

    def __init__(self, sprite_prop, moving_prop):
        super().__init__(sprite_prop, starting_frame=0, frames_count=4)
        self.moving_prop = moving_prop
        self.active = True
        self.looping = True
        self.looking_dir = [1, 1]
        self.attach_own_player(AnimationPlayer(self.frames_count, duration=2))
        self.last_state = self.EntityState.IDLE

    def update(self, *args, dt, **kwargs):
        super().update(*args, dt=dt, **kwargs)
        direction = self.moving_prop.direction

        entity_state = self.EntityState.get_state(self.moving_prop)
        start_idx_x = 0 if entity_state == self.EntityState.IDLE else 4
        self.frames_count = 4 if entity_state == self.EntityState.IDLE else 8
        if self.own_player:
            self.own_player.duration = 8 if entity_state == self.EntityState.IDLE else 2 * self.moving_prop.speed / 1000
        # todo vary duration

        if direction.x < 0:
            self.looking_dir[0] = -1
        if direction.x > 0:
            self.looking_dir[0] = 1
        if direction.y < 0:
            self.looking_dir[1] = -1
        if direction.y > 0:
            self.looking_dir[1] = 1

        if self.looking_dir == [1, -1]:
            start_idx_y = 0
        elif self.looking_dir == [-1, -1]:
            start_idx_y = 2
        elif self.looking_dir == [-1, 1]:
            start_idx_y = 3
        else:
            start_idx_y = 1

        last_starting_frame = self.starting_frame

        self.starting_frame = start_idx_y * self.sprite_prop.image_meta.columns_count + start_idx_x  # todo
        if last_starting_frame != self.starting_frame:
            self.current_frame = self.starting_frame  # todo change!!!!

        debug_msg = f'MoveAnim: dir: {direction}, state: {entity_state}, looking_dir: {self.looking_dir},'
        debug_msg += f'frames: {self.starting_frame}-{self.starting_frame + self.frames_count} [{start_idx_x}, {start_idx_y}], curr: {self.current_frame}'
        Debugger.print(debug_msg)


class SpriteProperty(RenderProperty, UpdateProperty):
    class Layer(Enum):  # todo refactor somhere
        FLOOR = 0
        DETAILS = 1
        OBJECTS = 2

        @property
        def layer_id(self):
            return self.value

    def __init__(self, image_meta, world, position, visible=False, stack_layer=Layer.FLOOR):
        self.image_meta = image_meta
        self.world = world
        self.stack_layer = stack_layer
        self._sprite = Sprite()  # no group at start = visible False
        self._sprite.image = self.image_meta.image
        self._sprite.rect = Rect(position, self.dimensions)
        self.visible = visible
        self.clip_rect = Rect((0, 0), self.dimensions)
        self._image_index = -1
        self.image_index = 0  # too to set index and update clip_rect

    def __del__(self):
        self.visible = False

    @property
    def rect(self):
        return self._sprite.rect

    @property
    def dimensions(self):
        return self.image_meta.tile_size

    @property
    def image(self):
        return self._sprite.image

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, vis):
        self._visible = vis
        if self._visible:
            WorldRenderer.add_visible_object(self)
        else:
            WorldRenderer.remove_visible_object(self)

    @property
    def image_index(self):
        return self._image_index

    @image_index.setter
    def image_index(self, index):
        if self._image_index != index:
            self._image_index = index
            img_col, img_row = self.image_meta.column_row_from_index(index)
            self.clip_rect.x = self.rect.w * img_col
            self.clip_rect.y = self.rect.h * img_row

    def update(self, *args, **kwargs):
        fov_rect = self.world.camera.fov_rect
        should_be_visible = fov_rect.colliderect(self.rect)
        if not self.visible and should_be_visible:
            self.visible = True
        elif self.visible and not should_be_visible:
            self.visible = False

    def render(self, *args, **kwargs):
        if self.visible and DEBUG_VISIBLE_OBJECTS:
            Debugger.rect(self._sprite.rect, 'Red')
            self._sprite.update(*args, **kwargs)


class CollisionProperty(UpdateProperty, RenderProperty):
    """This property doesn't mean object checks collison with other objects.
    Can stand still, only moving objects activate collision check"""
    INFLATION = -6

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
        if self.active and DEBUG_COLLISION_BLOCKS:
            Debugger.rect(self.hitbox, 'Blue')


class MovingProperty(UpdateProperty):
    def __init__(self, collision_prop, world, ignore_collisions=False):
        self.speed = 100
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
            if DEBUG_COLLISION_BLOCKS:
                for obstacle in obstacles:
                    Debugger.rect(obstacle.hitbox, 'Yellow', 2)

            translation = direction * self.speed * dt
            self.obstacles_hit, translation = self.eval_collision(translation, obstacles)

            self.collision_prop.parent_rect.x += translation[0]
            self.collision_prop.parent_rect.y += translation[1]

            if DEBUG_COLLISION_BLOCKS:
                for obstacle in self.obstacles_hit:
                    Debugger.rect(obstacle.hitbox, 'Yellow', 3)

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
