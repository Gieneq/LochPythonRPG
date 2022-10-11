import pygame
import sys
from .settings import *
from . import debug
from world.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(WINDOW_TITLE)

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()


            self.screen.fill('black')
            self.level.run()
            debug.text(msg=f"FPS:{round(self.clock.get_fps(),1)}")
            pygame.display.update()
            self.clock.tick(FPS)
