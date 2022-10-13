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

        # setup world
        self.world = World()

        # setup renderers
        renderer.WorldRenderer.init()
        renderer.WorldRenderer.attach(self.world)
        renderer.DebugRenderer.attach(Debugger)

    @staticmethod
    def exit():
        print('Quiting')
        pygame.quit()
        sys.exit()

    def input(self):
        Debugger.print(f"Mouse: {pygame.mouse.get_pos()}")
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
        benchmarking_timer = NanoTimer()
        benchmark_delta_s = {
            'input': 0,
            'update': 0,
            'render': 0,
        }
        benchmarking_msg = ''
        while True:
            benchmarking_timer.start()
            self.input()
            benchmark_delta_s['input'] = benchmarking_timer.start().delta_time_ns
            self.update(update_timer.last_delta_s)
            benchmark_delta_s['update'] = benchmarking_timer.start().delta_time_ns
            Debugger.print(benchmarking_msg)
            self.render()
            benchmark_delta_s['render'] = benchmarking_timer.start().delta_time_ns
            benchmarking_msg = f"Bench: {[(k, str(round(v*1e-6,3)).rjust(6, '0')) for k, v in benchmark_delta_s.items()]}[ms]"
            self.clock.tick(FPS)
            update_timer.start()
