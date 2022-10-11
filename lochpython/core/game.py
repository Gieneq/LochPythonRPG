import pygame
import sys
from .settings import *
from . import debug
from world.level import Level
from time import time_ns

from .utils import NanoTimer


def check_if_exit(on_exit_function):
    for event in pygame.event.get():
        # TODO what are other events?
        if event.type == pygame.QUIT:
            on_exit_function()
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        on_exit_function()


class Game:
    def __init__(self):
        pygame.init()

        # setup window
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # setup game update
        self.clock = pygame.time.Clock()

        self.level = Level()

    @staticmethod
    def exit():
        print('Quiting')
        pygame.quit()
        sys.exit()

    def input(self):
        check_if_exit(Game.exit)

    def update(self, dt):
        debug.text(msg=f"FPS:{round(self.clock.get_fps(), 1)}, dt: {dt}")

    def render(self):
        self.screen.fill('black')
        self.level.run()
        pygame.display.update()

    def start(self):
        update_timer = NanoTimer()
        while True:
            self.input()
            self.update(update_timer.last_delta_s)
            self.render()
            self.clock.tick(FPS)
            update_timer.start()
