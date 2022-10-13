import pygame

from core.debug import Debugger
from core.settings import *
from pygame.sprite import Group

# todo przenies grupy do renderera, world moze trzymac wlasne listy np chunkow - bedzie w nich na pewno wiecej obiektow
# world moze miec cos wspolnego dla entity player/cosinnego

# wworldrenderer ma miec metode sort, ktora bedzie wyzwalana podczas ruchu entity, dodawnaia entity do widzialnych obiektow

#dodanie entity do swiata to nie to samo co zrobienie go widzialnym

class WorldRenderer:
    display_surface = None
    world = None
    visible_objects = Group() # todo own implemetation

    @classmethod
    def init(cls):
        cls.display_surface = pygame.display.get_surface()

    @classmethod
    def attach(cls, world):
        cls.world = world

    @classmethod
    def render(cls):
        # TODO camera stuff
        # if cls.world:
        cls.visible_objects.draw(cls.display_surface)
        Debugger.print(f'Visible_objects count: {len(cls.visible_objects)}')
        Debugger.print(f'Obstacle_objects count: {len(cls.world.obstacle_objects)}')

    @classmethod
    def sort_visibility(cls):
        Debugger.print('Sorting')
        cls.visible_objects = Group(sorted(cls.visible_objects, key=lambda x: x.rect.centery))


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





# class YSortCameraGroup(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__()
#         self.display_surface = pygame.display.get_surface()
#         self.half_width = self.display_surface.get_width() // 2
#         self.half_height = self.display_surface.get_height() // 2
#         self.offset = pygame.math.Vector2()
#
#         self.floor_surf = pygame.image.load('./data/graphics/tilemap/ground.png')
#         self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
#
#     def custom_draw(self, player):
#         # getting the offset
#         self.offset.x = player.rect.centerx - self.half_width
#         self.offset.y = player.rect.centery - self.half_height
#
#         offset_position = self.floor_rect.topleft - self.offset
#         self.display_surface.blit(self.floor_surf, offset_position)
#
#         for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
#             offset_position = sprite.rect.topleft - self.offset
#             self.display_surface.blit(sprite.image, offset_position)

