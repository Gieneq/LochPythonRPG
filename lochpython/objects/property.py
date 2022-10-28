from random import randint
from enum import Enum, auto

import pygame
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Sprite
from abc import ABC, abstractmethod

import core.timers
from core.settings import TILESIZE, DEBUG_VISIBLE_OBJECTS, DEBUG_COLLISION_BLOCKS

from core.debug import Debugger
from core.renderer import WorldRenderer, SkyRenderer
from core.utils import generate_span_rect
from core.timers import global_timers, AnimationController, Timer


# from objects.go import GameObject


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


class LightSourceProperty(UpdateProperty):
    def __init__(self, parent_rect, relative_position, strength, active=True):
        self.parent_rect = parent_rect
        self.relative_position = relative_position
        self.position = parent_rect.x, parent_rect.y
        self.strength = strength
        self.active = active
        self.deviation_timer = core.timers.global_timers.get_timer(100)
        self.deviation_timer.attach(self.rand_deviation)
        self.deviation = (0, 0)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, ac):
        self._active = ac
        if self._active:
            SkyRenderer.add_point_light(self)
        else:
            SkyRenderer.remove_point_light(self)

    def rand_deviation(self):
        self.deviation = randint(-1, 1), randint(-1,1)

    def update(self, *args, **kwargs):
        if self._active:
            self.position = self.parent_rect[0] + self.relative_position[0] + self.deviation[0], self.parent_rect[1] + \
                            self.relative_position[1] + self.deviation[1]
            # print(self.position)


class AnimationProperty(UpdateProperty):

    def __init__(self, sprite_prop, looping=True, active=False, keyframes=None):
        self.sprite_prop = sprite_prop
        self.keyframes = [] if not keyframes else keyframes
        self.looping = looping
        self.active = active
        self.parent_ctrl = None
        self._current_frame = 0

    def attach_to_controller(self, controller):
        if self.set_frame not in controller.handlers:
            controller.handlers.append(self.set_frame)
            self.parent_ctrl = controller

    def detach_from_controller(self):
        self.parent_ctrl.handlers.remove(self.set_frame)
        self.parent_ctrl = None

    @property
    def current_frame(self):
        return self._current_frame

    def set_frame(self, frame_index):
        self.current_frame = frame_index

    @current_frame.setter
    def current_frame(self, frame_index):
        self._current_frame = frame_index
        self.sprite_prop.image_index = self.keyframes[frame_index].tile_id

    @property
    def frames_count(self):
        return len(self.keyframes)

    def next_frame(self):
        next_index = self.current_frame + 1
        if next_index >= self.frames_count:
            next_index = next_index % self.frames_count if self.looping else self.frames_count - 1
        self.current_frame = next_index

    def update(self, *args, dt, **kwargs):
        pass
        # # todo and not...
        # if self.active and self.parent_timer:
        #     self.parent_timer.update(*args, dt=dt, **kwargs)


class MovementAnimationProperty(AnimationProperty):
    class EntityState(Enum):
        IDLE = 0
        MOVING = 1

        @classmethod
        def get_state(cls, moving_prop):
            return cls.MOVING if moving_prop.direction.magnitude() != 0 else cls.IDLE

    def __init__(self, sprite_prop, moving_prop):
        super().__init__(sprite_prop)
        self.moving_prop = moving_prop
        self.active = True
        self.looping = True
        self.looking_dir = [1, 1]
        self.animation_timer = Timer(2000 / self.frames_count, active=True)
        self.animation_ctrl = AnimationController(self.frames_count)
        self.attach_to_controller(self.animation_ctrl)
        self.last_state = self.EntityState.IDLE

    def update(self, *args, dt, **kwargs):
        super().update(*args, dt=dt, **kwargs)
        direction = self.moving_prop.direction

        entity_state = self.EntityState.get_state(self.moving_prop)
        start_idx_x = 0 if entity_state == self.EntityState.IDLE else 4
        self.frames_count = 4 if entity_state == self.EntityState.IDLE else 8
        if self.parent_ctrl:
            self.parent_ctrl.duration = 8 if entity_state == self.EntityState.IDLE else 2 * self.moving_prop.speed / 1000
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

    def __init__(self, image_data, world, position, visible=False, z_index=0, dst_layer=None):
        """
        Tile size from image_data
        """
        self.image_data = image_data
        self.world = world
        self.z_index = z_index
        if dst_layer is None:
            # GameObject.GOType.OBJECTS
            # todo
            self.dst_layer = 0
        else:
            self.dst_layer = dst_layer
        self._sprite = Sprite()
        self._sprite.image = self.image_data.surface
        self._sprite.rect = Rect(position, self.dimensions)
        self.visible = visible
        self.clip_rect = Rect((0, 0), self.dimensions)
        self._image_index = -1
        self.image_index = 0

    def __del__(self):
        self.visible = False

    @property
    def rect(self):
        return self._sprite.rect

    @property
    def dimensions(self):
        return self.image_data.tile_size

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
            img_col, img_row = self.image_data.column_row_from_local_index(index)
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
        self.hitboxes = None
        self.group_hitbox = None
        self.fixed_hitboxes = []
        self._hitbox_method = self._use_generic_hitbox
        self.world = world
        self.active = active
        self.update_hitboxes()

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

    def _use_generic_hitbox(self):
        return [Rect(self.parent_rect).inflate(0, CollisionProperty.INFLATION)]

    def _use_fixed_hitboxes(self):
        return [Rect(fixed_hitbox).move(self.parent_rect.x, self.parent_rect.y) for fixed_hitbox in self.fixed_hitboxes]

    def add_hitbox(self, hitbox_rect):
        self.fixed_hitboxes.append(Rect(hitbox_rect))
        self._hitbox_method = self._use_fixed_hitboxes
        self.update_hitboxes()

    def add_hitboxes(self, hitbox_rects):
        for hb in hitbox_rects:
            self.add_hitbox(hb)

    def update_hitboxes(self):
        if self.active:
            self.hitboxes = self._hitbox_method()
            self.group_hitbox = generate_span_rect(self.hitboxes)

    def update(self, *args, **kwargs):
        if self.active:
            self.update_hitboxes()

    def render(self, *args, **kwargs):
        if self.active and DEBUG_COLLISION_BLOCKS:
            for hitbox in self.hitboxes:
                Debugger.rect(hitbox, 'Blue')
            # Debugger.rect(self.group_hitbox, 'Green')


class MovingProperty(UpdateProperty):
    def __init__(self, collision_prop, world, ignore_collisions=False):
        self.speed = 100
        self.world = world
        self.collision_prop = collision_prop
        self.direction = Vector2(0, 0)
        self.ignore_collisions = ignore_collisions
        self.obstacles_hit = []

    def eval_collision(self, translation, obstacles):
        # todo oneday if neede - use list of hitboxes
        from_point = Vector2(self.collision_prop.group_hitbox.topleft)
        o_encountered_x = self.eval_collision_x(translation, obstacles)
        o_encountered_y = self.eval_collision_y(translation, obstacles)
        to_point = Vector2(self.collision_prop.group_hitbox.topleft)
        return list(set(o_encountered_x + o_encountered_y)), to_point - from_point

    def eval_collision_x(self, translation, obstacles):
        obstacles_encountered = []
        self.collision_prop.group_hitbox.x += translation[0]
        for obstacle in obstacles:
            for hitbox in obstacle.hitboxes:
                if hitbox.colliderect(self.collision_prop.group_hitbox):
                    if obstacle not in obstacles_encountered:
                        obstacles_encountered.append(obstacle)
                    if translation[0] > 0:
                        self.collision_prop.group_hitbox.right = hitbox.left
                    if translation[0] < 0:
                        self.collision_prop.group_hitbox.left = hitbox.right
        return obstacles_encountered

    def eval_collision_y(self, translation, obstacles):
        obstacles_encountered = []
        self.collision_prop.group_hitbox.y += translation[1]
        for obstacle in obstacles:
            for hitbox in obstacle.hitboxes:
                if hitbox.colliderect(self.collision_prop.group_hitbox):
                    if obstacle not in obstacles_encountered:
                        obstacles_encountered.append(obstacle)
                    if translation[1] > 0:
                        self.collision_prop.group_hitbox.bottom = hitbox.top
                    if translation[1] < 0:
                        self.collision_prop.group_hitbox.top = hitbox.bottom
        return obstacles_encountered

    def update(self, *args, dt, **kwargs):
        direction = self.direction.copy()  # maybe not necesery
        if direction.magnitude() != 0:
            direction = direction.normalize()

            obstacles = self.world.get_nearby_obstacles(self.collision_prop)
            Debugger.print('Potential obstacles count', len(obstacles))
            if DEBUG_COLLISION_BLOCKS:
                for obstacle in obstacles:
                    Debugger.rect(obstacle.group_hitbox, 'Yellow', 2)

            translation = direction * self.speed * dt

            self.obstacles_hit, translation = self.eval_collision(translation, obstacles)

            self.collision_prop.parent_rect.x += translation[0]
            self.collision_prop.parent_rect.y += translation[1]

            if DEBUG_COLLISION_BLOCKS:
                for obstacle in self.obstacles_hit:
                    Debugger.rect(obstacle.group_hitbox, 'Yellow', 3)

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
    LIGHT_SOURCE = LightSourceProperty
