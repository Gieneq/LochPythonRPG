import pygame
from pygame.sprite import Sprite
from core.settings import TILESIZE
from core.renderer import WorldRenderer
# from entity.entity import Entity


class AnimationController:
    def __init__(self, frames_count=4, total_duration_s=1, indices=None, running=True):
        self.frames_count = frames_count
        self.total_duration_s = total_duration_s
        self.interval = self.total_duration_s / self.frames_count
        self.current_frame = 0
        self.accumulated_time_s = 0

        if indices is not None and len(indices) != self.frames_count:
            raise IndexError(f"Animation cannot be controller, number of indices in list is not equal frames_count.")
        self.indices = indices if indices else list(range(self.frames_count))

        self.running = running

    def update(self, dt, next_function=None):
        if self.running:
            self.accumulated_time_s += dt

            if self.accumulated_time_s > self.interval:
                self.accumulated_time_s -= self.interval
                self.current_frame = (self.current_frame + 1) % self.frames_count
                if next_function:
                    next_function(frame=self.current_frame, frames_count=self.frames_count)


#TODO
# - zmieniac draw_rect na bazie wybranego indeksu,
# - kontroler animacji steruje wybranym indeksem -> draw_rect
# - zrobic baze ilustracji w loaderze
# - player, entity, tile musza miec cos wspolnego
# - zrobic klase AnimatedSprite
# - nie wiem czy da sie wybrac czy dziedzicyz po sprite czy animated sprite
# - ale moze Factory zalatwi sprawe tworzenia kafelkow/entity, trzeba tylko miec
# - jakiegos JSONA z opisem

# class Tile(Sprite):
    # def __init__(self, starting_pos, image, indices=[1], visible=True, animated=False, dimensions=(TILESIZE, TILESIZE)):
    #     super().__init__()
    #     # TODO IMAGE DO JAKIEJS BAZY I TU W ARGUMENCIE
    #     self.image = image  # pygame.image.load('./data/graphics/rock.png').convert_alpha() #
    #     self.rect = pygame.Rect(starting_pos, dimensions)
    #     self.hitbox = self.rect.inflate(0, -26)
    #     self.set_visible(visible)
    #
    #     self.draw_rect = pygame.Rect((0,0), dimensions)
    #     self.animation = None if not animated else AnimationController()
    #
    # def update(self, dt, *args, **kwargs):
    #     super().update(*args, **kwargs)
    #     if self.animation:
    #         pass
    #
    # def set_visible(self, visible):
    #     if visible:
    #         self.add(WorldRenderer.visible_objects)
    #     else:
    #         self.remove(WorldRenderer.visible_objects)
