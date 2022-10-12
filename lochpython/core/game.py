import pygame
pygame.init()

import sys
from core.settings import *
from core.debug import Debugger
from world.world import World
import core.renderer as renderer

from core.utils import NanoTimer


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

        #setup world
        self.world = World()

        #setup renderers
        renderer.WorldRenderer.init()
        renderer.WorldRenderer.attach(self.world)
        renderer.DebugRenderer.attach(Debugger)

    @staticmethod
    def exit():
        print('Quiting')
        pygame.quit()
        sys.exit()

    def input(self):
        check_if_exit(Game.exit)

    def update(self, dt):
        Debugger.print("FPS = ", round(self.clock.get_fps(), 1), " Hz", sep="")
        Debugger.print("Dt = ", round(1e3 * dt, 3), " ms", sep="")
        self.world.update(dt)

    def render(self):
        self.screen.fill('black')

        # use all renders
        renderer.WorldRenderer.render()
        renderer.DebugRenderer.render()

        pygame.display.update()

    def start(self):
        update_timer = NanoTimer()
        while True:
            self.input()
            self.update(update_timer.last_delta_s)
            self.render()
            self.clock.tick(FPS)
            update_timer.start()
