from lochpython.core.settings import *
from lochpython.core.timers import global_timers

import sys
from lochpython.core.debug import Debugger
from lochpython.core.timers import AnimationController
from lochpython.world.world import World
import lochpython.core.renderer as renderer

from lochpython.core.utils import NanoTimer, ValueFilter


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
        pygame.display.set_caption(WINDOW_TITLE)  # tod omove to settings

        # setup game update
        self.clock = pygame.time.Clock()

        # setup world
        self.world = World()

        # setup renderers
        renderer.MainRenderer.init()
        renderer.SkyRenderer.init()
        renderer.WorldRenderer.init()
        renderer.WorldRenderer.attach(self.world)
        renderer.SkyRenderer.attach_camera(self.world.camera)
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
        global_timers.update(dt=dt)
        Debugger.print(f"AnimationTimers: {AnimationController.total_count}")
        Debugger.print("FPS = ", round(self.clock.get_fps(), 1), " Hz", sep="")
        Debugger.print("Dt = ", round(1e3 * dt, 3), " ms", sep="")
        Debugger.print(f'Visible_objects count: {renderer.WorldRenderer.visible_objects_count}')
        Debugger.print(f'Basement count: {self.world.basement_tiles_count}')
        Debugger.print(f'Objects count: {self.world.objects_count}')
        Debugger.print(f'Light sources: {len(renderer.SkyRenderer.light_sources)}')
        Debugger.print(f'Obstacle_objects count: {self.world.limit_blocks_count}')
        self.world.update(dt)

    def render(self):
        self.world.render()
        renderer.MainRenderer.render()

    def start(self):
        update_timer = NanoTimer(init_delta_s=1 / FPS)
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
            sum_time = sum([v.median * 1e-6 for v in benchmark_delta_s.values()])
            benchmarking_msg = f"Bench: {[(k, str(round(v.median * 1e-6, 1)).rjust(6, '0')) for k, v in benchmark_delta_s.items()]}, total: {round(sum_time, 1)}[ms]"
            self.clock.tick(FPS)
            update_timer.start()
