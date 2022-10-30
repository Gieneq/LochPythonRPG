import math
import time
from functools import reduce

import pygame.color
from pygame.rect import Rect

from lochpython.core.debug import Debugger
from lochpython.core.settings import *
from pygame.math import Vector2

from lochpython.core.utils import sub_tuples_2D, add_tuples_2D


class RenderingGroup(list):
    def __init__(self, camera=Vector2()):
        super().__init__()
        self.camera = camera

    def attach_camera(self, camera):
        self.camera = camera

    def draw(self, surface):
        translation = sub_tuples_2D(self.camera, (HALF_RENDERING_WIDTH, HALF_RENDERING_HEIGHT))
        for sprite_prop in self:
            sprite_pos = sub_tuples_2D(sprite_prop.rect.topleft, translation)
            image_data = sprite_prop.image_data
            sprite_clip_rect = sprite_prop.clip_rect
            # scaled_image = pygame.transform.scale(sprite_image, (w,h))
            surface.blit(image_data.surface, sprite_pos, sprite_clip_rect)


class MainRenderer:
    display_surface = None
    world_surface = None
    scale = SCALE
    rendering_width = RENDERING_WIDTH
    rendering_height = RENDERING_HEIGHT
    rendering_rect = pygame.Rect((0, 0), (RENDERING_WIDTH, RENDERING_HEIGHT))

    @classmethod
    def init(cls):
        cls.display_surface = pygame.display.get_surface()
        cls.rendering_width = cls.display_surface.get_width() / cls.scale  # todo int?
        cls.rendering_height = cls.display_surface.get_height() / cls.scale
        cls.world_surface = pygame.Surface((cls.rendering_width, cls.rendering_height),
                                           depth=cls.display_surface.get_bitsize())
        cls.rendering_rect = pygame.Rect((0, 0), (cls.rendering_width, cls.rendering_height))

    @classmethod
    def render(cls):
        cls.display_surface.fill('black')
        cls.world_surface.fill('black')
        WorldRenderer.render()
        SkyRenderer.render()
        DebugRenderer.render_in_world()

        pygame.transform.scale(surface=cls.world_surface, size=(DISPLAY_WIDTH, DISPLAY_HEIGHT),
                               dest_surface=cls.display_surface)
        cls.display_surface.blit(cls.display_surface, cls.rendering_rect)

        DebugRenderer.render_in_gui()
        pygame.display.update()


class WorldRenderer:
    world = None
    basement_sprites = RenderingGroup()
    # details_objects = RenderingGroup()
    objects_sprites = RenderingGroup()
    stack = [basement_sprites, objects_sprites]

    @classmethod
    def init(cls):
        pass

    @classmethod
    def attach(cls, world):
        cls.world = world

    @classmethod
    def add_visible_object(cls, sprite_prop):
        dst_layer = sprite_prop.dst_layer
        # z_index = sprite_prop.z_index
        cls.stack[dst_layer].append(sprite_prop)

    @classmethod
    def remove_visible_object(cls, sprite_prop):
        dst_layer = sprite_prop.dst_layer
        if sprite_prop in cls.stack[dst_layer]:
            cls.stack[dst_layer].remove(sprite_prop)

    @classmethod
    def sort_order(cls):
        Debugger.print('Renderer sorting')
        cls.objects_sprites.sort(key=lambda sp_prop: (sp_prop.rect.bottom, sp_prop.z_index))

    @classmethod
    def render(cls):
        for layer in cls.stack:
            layer.attach_camera(cls.world.camera)
            layer.draw(MainRenderer.world_surface)

    @classmethod
    @property
    def visible_objects_count(cls):
        return reduce(lambda a, b: a + len(b), cls.stack, 0)


class SkyRenderer:
    POINT_LIGHT_PATH = 'data/lighting/point_light.png'
    camera = None
    sky_surface = None
    point_light_images = dict()
    light_sources = []
    darknes = 0

    @classmethod
    def attach_camera(cls, camera):
        cls.camera = camera

    @classmethod
    def get_point_light_graphic(cls, level=7, color=(255,255,255)):
        key = level, color
        if key in cls.point_light_images:
            return cls.point_light_images[key]

        print('Building light image', level, color)
        src_image = pygame.image.load(cls.POINT_LIGHT_PATH)
        src_size, src_depth = (src_image.get_width(), src_image.get_height()), src_image.get_bitsize()
        inv_surface = pygame.Surface(src_size, depth=src_depth)
        inv_surface.fill(color)
        # inv_surface.fill(pygame.color.Color('White'))
        inv_surface.blit(src_image, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

        min_size = POINT_LIGHT_MIN_IMAGE_SIZE
        levels_count = POINT_LIGHT_STRENGTH_LEVELS

        scale_factor = level / levels_count
        img_width = int(min_size[0] + scale_factor * (src_size[0] - min_size[0]))
        img_height = int(min_size[1] + scale_factor * (src_size[1] - min_size[1]))
        result = pygame.transform.scale(inv_surface, (img_width, img_height))
        cls.point_light_images[key] = result
        return result

    @classmethod
    def init(cls):
        width, height = MainRenderer.rendering_width, MainRenderer.rendering_height
        cls.sky_surface = pygame.Surface((width, height), depth=MainRenderer.world_surface.get_bitsize())
        # cls.point_light_images = cls._load_point_light_graphics()
        # aww
        if not cls.light_sources:
            cls.light_sources = []
        # cls.light_sources.append()
        # print(cls.sky_surface)

    @classmethod
    def render(cls):
        channel_value = 180
        cls.sky_surface.fill((channel_value, channel_value, channel_value))
        for ls_prop in cls.light_sources:
            light_strength = ls_prop.strength
            light_color = ls_prop.color
            point_light_image = cls.get_point_light_graphic(light_strength, light_color)
            point_light_img_size = (point_light_image.get_width() // 2, point_light_image.get_height() // 2)
            light_pos = sub_tuples_2D(ls_prop.position, point_light_img_size)
            light_pos = sub_tuples_2D(light_pos, cls.camera)
            light_pos = add_tuples_2D(light_pos, (HALF_RENDERING_WIDTH, HALF_RENDERING_HEIGHT))
            cls.sky_surface.blit(point_light_image, light_pos, special_flags=pygame.BLEND_RGB_SUB)
        MainRenderer.world_surface.blit(cls.sky_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

    @classmethod
    def add_point_light(cls, light):
        if light not in cls.light_sources:
            cls.light_sources.append(light)

    @classmethod
    def remove_point_light(cls, light):
        if light in cls.light_sources:
            cls.light_sources.remove(light)


class DebugRenderer:
    font_size = 24
    numbering = True
    min_x, min_y = 10, 10

    step_y = int(font_size * 0.75)
    font = pygame.font.Font(None, font_size)
    _debugger = None
    camera = (0, 0)

    @classmethod
    def init(cls):
        pass

    @classmethod
    def attach(cls, debugger):
        cls._debugger = debugger

    @classmethod
    def attach_camera(cls, camera):
        cls.camera = camera

    @classmethod
    def render_in_gui(cls):
        if DEBUG:
            for i_y, line in enumerate(cls._debugger.debug_lines):
                line = f"{i_y}:   {line}" if cls.numbering else line
                text_surface = cls.font.render(line, True, 'White')
                x, y = cls.min_x, cls.min_y + i_y * cls.step_y
                text_rect = text_surface.get_rect(topleft=(x, y))
                pygame.draw.rect(MainRenderer.display_surface, 'Black', text_rect)
                MainRenderer.display_surface.blit(text_surface, text_rect)

            # consider extracting
            cls._debugger.clear_gui()

    @classmethod
    def render_in_world(cls):
        if DEBUG:
            translation = sub_tuples_2D(cls.camera, (HALF_RENDERING_WIDTH, HALF_RENDERING_HEIGHT))
            for rect, color, border in cls._debugger.rects:
                translated_rect = rect.move(-translation[0], -translation[1])
                pygame.draw.rect(MainRenderer.world_surface, color, translated_rect, border)

            # consider extracting
            cls._debugger.clear_rects()
