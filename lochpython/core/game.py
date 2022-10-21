from core.settings import *

import sys
from core.debug import Debugger
from objects.property import AnimationPlayer
from world.world import World
import core.renderer as renderer

from core.utils import NanoTimer, ValueFilter


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
        pygame.display.set_caption(WINDOW_TITLE) #tod omove to settings

        # setup game update
        self.clock = pygame.time.Clock()

        # setup world
        self.world = World()

        # setup renderers
        renderer.MainRenderer.init()
        renderer.WorldRenderer.init()
        renderer.WorldRenderer.attach(self.world)
        renderer.DebugRenderer.init()
        renderer.DebugRenderer.attach(Debugger)
        renderer.DebugRenderer.attach_camera(self.world.camera)

    @staticmethod
    def exit():
        print('Quiting')
        pygame.quit()
        sys.exit()

    def input(self):
        Debugger.print(f"Mouse: {pygame.mouse.get_pos()}")
        check_if_exit(Game.exit)
        self.world.input()

    def update(self, dt):
        Debugger.print(f"AnimationTimers: {AnimationPlayer.total_players}")
        Debugger.print("FPS = ", round(self.clock.get_fps(), 1), " Hz", sep="")
        Debugger.print("Dt = ", round(1e3 * dt, 3), " ms", sep="")
        self.world.update(dt)

    def render(self):
        self.world.render()
        renderer.MainRenderer.render()


    def start(self):
        update_timer = NanoTimer(init_delta_s=1/FPS)
        benchmarking_timer = NanoTimer()
        benchmark_delta_s = {
            'input': ValueFilter(),
            'update': ValueFilter(),
            'render': ValueFilter(),
        }
        benchmarking_msg = ''
        while True:
            benchmarking_timer.start()
            self.input()
            benchmark_delta_s['input'].push_value(benchmarking_timer.start().last_delta_ns)
            self.update(update_timer.last_delta_s)
            benchmark_delta_s['update'].push_value(benchmarking_timer.start().last_delta_ns)
            Debugger.print(benchmarking_msg)
            self.render()
            benchmark_delta_s['render'].push_value(benchmarking_timer.start().last_delta_ns)
            benchmarking_msg = f"Bench: {[(k, str(round(v.median*1e-6,3)).rjust(6, '0')) for k, v in benchmark_delta_s.items()]}[ms]"
            self.clock.tick(FPS)
            update_timer.start()
