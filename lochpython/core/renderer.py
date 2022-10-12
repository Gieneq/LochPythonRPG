import pygame

from core.debug import Debugger
from core.settings import *


class WorldRenderer:
    display_surface = None
    world = None

    @classmethod
    def init(cls):
        cls.display_surface = pygame.display.get_surface()

    @classmethod
    def attach(cls, world):
        cls.world = world

    @classmethod
    def render(cls):
        # TODO camera stuff
        if cls.world:
            cls.world.visible_objects.draw(cls.display_surface)
            Debugger.print(f'Visible_objects count: {len(cls.world.visible_objects)}')


class DebugRenderer:
    font_size = 24
    numbering = True
    min_x, min_y = 10, 10

    step_y = int(font_size * 0.75)
    font = pygame.font.Font(None, font_size)
    _debugger = None

    @classmethod
    def attach(cls, debugger):
        cls._debugger = debugger

    @classmethod
    def render(cls):
        if DEBUG:
            display_surface = pygame.display.get_surface()
            for i_y, line in enumerate(cls._debugger.debug_lines):
                line = f"{i_y}:   {line}" if cls.numbering else line
                text_surface = cls.font.render(line, True, 'White')
                x, y = cls.min_x, cls.min_y + i_y * cls.step_y
                text_rect = text_surface.get_rect(topleft=(x, y))
                pygame.draw.rect(display_surface, 'Black', text_rect)
                display_surface.blit(text_surface, text_rect)

            # consider extracting
            cls._debugger.clear()
