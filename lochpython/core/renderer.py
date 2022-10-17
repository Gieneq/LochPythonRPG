import pygame

from core.debug import Debugger
from core.settings import *
from pygame.math import Vector2

from core.utils import sub_tuples_2D

pygame.init() #todo meh

class RenderingGroup(list):
    def __init__(self, camera=Vector2()):
        super().__init__()
        self.camera = camera

    def attach_camera(self, camera):
        self.camera = camera

    def draw(self, surface):
        Debugger.print(f"Cam: {self.camera}")
        translation = sub_tuples_2D(self.camera, (HALF_WIDTH, HALF_HEIGHT))
        for sprite_prop in self:
            sprite_pos = sub_tuples_2D(sprite_prop.rect.topleft, translation)
            sprite_image = sprite_prop.image
            sprite_clip_rect = sprite_prop.clip_rect
            surface.blit(sprite_image, sprite_pos, sprite_clip_rect)


class WorldRenderer:
    display_surface = None
    world = None
    visible_objects = RenderingGroup()  # todo own implemetation

    @classmethod
    def init(cls):
        cls.display_surface = pygame.display.get_surface()

    @classmethod
    def attach(cls, world):
        cls.world = world

    @classmethod
    def render(cls):
        cls.visible_objects.attach_camera(cls.world.camera)
        cls.visible_objects.draw(cls.display_surface)
        Debugger.print(f'Visible_objects count: {len(cls.visible_objects)}')
        Debugger.print(f'Obstacle_objects count: {len(cls.world.limit_blocks)}')

    @classmethod
    def sort_order(cls):
        Debugger.print('Sorting')
        sorted_objects = sorted(cls.visible_objects, key=lambda x: x.rect.centery) #todo
        cls.visible_objects.clear()
        cls.visible_objects.extend(sorted_objects)


class DebugRenderer:
    display_surface = None
    font_size = 24
    numbering = True
    min_x, min_y = 10, 10

    step_y = int(font_size * 0.75)
    font = pygame.font.Font(None, font_size)
    _debugger = None
    camera = (0, 0)

    @classmethod
    def init(cls):
        cls.display_surface = pygame.display.get_surface()

    @classmethod
    def attach(cls, debugger):
        cls._debugger = debugger

    @classmethod
    def attach_camera(cls, camera):
        cls.camera = camera

    @classmethod
    def render(cls):
        if DEBUG:
            translation = sub_tuples_2D(cls.camera, (HALF_WIDTH, HALF_HEIGHT))
            for rect, color, border in cls._debugger.rects:
                translated_rect = rect.move(-translation[0], -translation[1])
                pygame.draw.rect(cls.display_surface, color, translated_rect, border)

            for i_y, line in enumerate(cls._debugger.debug_lines):
                line = f"{i_y}:   {line}" if cls.numbering else line
                text_surface = cls.font.render(line, True, 'White')
                x, y = cls.min_x, cls.min_y + i_y * cls.step_y
                text_rect = text_surface.get_rect(topleft=(x, y))
                pygame.draw.rect(cls.display_surface, 'Black', text_rect)
                cls.display_surface.blit(text_surface, text_rect)

            # consider extracting
            cls._debugger.clear()
