from functools import reduce

from lochpython.core.debug import Debugger
from lochpython.core.settings import *
from pygame.math import Vector2

from core.utils import sub_tuples_2D


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
        # cls.gui_surface.
        # cls.rendering_surface.f

        # cls.display_surface = pygame.display.get_surface()
        # cls.rendering_surface = pygame.transform.chop(cls.display_surface, Rect((0,0), (HALF_WIDTH//2, HALF_HEIGHT//2)))
        # cls.world_surface = cls.display_surface.copy()
        print(cls.display_surface)
        print(cls.world_surface)
        # print(cls.display_surface == screen)

    @classmethod
    def render(cls):
        cls.display_surface.fill('black')
        cls.world_surface.fill('black')
        WorldRenderer.render()
        DebugRenderer.render_in_world()

        # pygame.transform.scale2x(surface=cls.world_surface, dest_surface=cls.display_surface)
        # cls.display_surface.blit(cls.display_surface, cls.rendering_rect)
        pygame.transform.scale(surface=cls.world_surface, size=(DISPLAY_WIDTH, DISPLAY_HEIGHT),
                               dest_surface=cls.display_surface)
        cls.display_surface.blit(cls.display_surface, cls.rendering_rect)

        DebugRenderer.render_in_gui()
        pygame.display.update()


class WorldRenderer:
    world = None
    floor_objects = RenderingGroup()
    details_objects = RenderingGroup()
    entity_objects = RenderingGroup()
    stack = [floor_objects, details_objects, entity_objects]

    @classmethod
    def init(cls):
        pass

    @classmethod
    def attach(cls, world):
        cls.world = world

    @classmethod
    def add_visible_object(cls, sprite_prop):
        layer_id = sprite_prop.stack_layer.layer_id
        cls.stack[layer_id].append(sprite_prop)

    @classmethod
    def remove_visible_object(cls, sprite_prop):
        layer_id = sprite_prop.stack_layer.layer_id
        if sprite_prop in cls.stack[layer_id]:
            cls.stack[layer_id].remove(sprite_prop)

    @classmethod
    def render(cls):
        for layer in cls.stack:
            layer.attach_camera(cls.world.camera)
            layer.draw(MainRenderer.world_surface)

    @classmethod
    def sort_order(cls):
        Debugger.print('Sorting')
        sorted_objects = sorted(cls.entity_objects, key=lambda x: x.rect.centery)  # todo
        cls.entity_objects.clear()
        cls.entity_objects.extend(sorted_objects)

    @classmethod
    @property
    def visible_objects_count(cls):
        return reduce(lambda a, b: a + len(b), cls.stack, 0)


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
