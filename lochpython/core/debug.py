import pygame
from .settings import *

pygame.init()


class DebugWriter:
    fontsize = 24
    numbering = True
    min_x = 10
    min_y = 10
    step_y = int(fontsize*0.75)
    _debug_lines = []
    font = pygame.font.Font(None, fontsize)

    @classmethod
    def print(cls, *objects, sep=', '):
        if DEBUG:
            cls._debug_lines.append(sep.join([str(obj) for obj in objects]))

    @classmethod
    def render(cls):
        if DEBUG:
            display_surface = pygame.display.get_surface()
            for i_y, line in enumerate(cls._debug_lines):
                line = f"{i_y}:   {line}" if cls.numbering else line
                text_surface = cls.font.render(line, True, 'White')
                x, y = cls.min_x, cls.min_y + i_y * cls.step_y
                text_rect = text_surface.get_rect(topleft=(x, y))
                pygame.draw.rect(display_surface, 'Black', text_rect)
                display_surface.blit(text_surface, text_rect)
            cls._debug_lines.clear()