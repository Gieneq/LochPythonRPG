class Timer:
    def __init__(self, interval=1000, active=False, parent=None):
        self.interval = interval
        self.active = active
        self.handlers = []
        self.accumulated_time = 0
        self.parent = parent

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, itrval):
        self._interval = itrval/1000

    def triggered_by_parent(self, parent):
        self.active = False
        self.parent = parent

    def tick(self):
        for handler in self.handlers:
            handler()

    def attach(self, handler):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def detach(self, handler):
        if handler in self.handlers:
            self.handlers.remove(handler)

    def update(self, *args, dt=0, **kwargs):
        if self.active:
            self.accumulated_time += dt
            # print(self.accumulated_time, self.interval)
            if self.accumulated_time > self.interval:
                self.accumulated_time -= self.interval
                # print(f"{self}, tick")
                self.tick()

    def __str__(self):
        return f"T:{self._interval}"


class GlobalTimers:
    instance = None

    def __init__(self):
        self.timers = {}
        self.get_timer(100)
        self.get_timer(500)
        self.get_timer(1000)

    def update(self, *args, dt=0, **kwargs):
        for gt in self.timers.values():
            gt.update(dt=dt)

    def get_timer(self, interval):
        if interval in self.timers.keys():
            return self.timers[interval]
        new_timer = Timer(interval=interval, active=True)
        self.timers[interval] = new_timer
        print(f'Timer {new_timer} created')
        return new_timer


if not GlobalTimers.instance:
    GlobalTimers.instance = GlobalTimers()
global_timers = GlobalTimers.instance


class AnimationController:
    ctrls_register = []

    def __init__(self, frames_count, active=True, handlers=None):
        self.frames_count = frames_count
        self.active = active
        self.handlers = handlers if handlers else []
        self._current_frame = 0
        AnimationController.ctrls_register.append(self)
        self.parent_timer = None

    def __del__(self):
        if self in AnimationController.ctrls_register:
            AnimationController.ctrls_register.remove(self)

    def attach_to_timer(self, timer=None, interval=None):
        if not self.parent_timer:
            if not timer:
                timer = global_timers.get_timer(interval)
            timer.handlers.append(self.next_frame)
            self.parent_timer = timer

    def detach_timer(self):
        if self.parent_timer:
            self.parent_timer.handlers.remove(self.next_frame)
            self.parent_timer = None

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, frame):
        self._current_frame = frame

    def next_frame(self):
        if self.active:
            self.current_frame = (self.current_frame + 1) % self.frames_count
            for handler in self.handlers:
                handler(self.current_frame)

    @classmethod
    @property
    def total_count(cls):
        return len(cls.ctrls_register)
    # refactor to singleton

    def __str__(self):
        return f"C:{self.frames_count}/{self.parent_timer}"


class GlobalControllers:
    instance = None

    def __init__(self):
        self.controllers = dict()
        self.get_controller(4, 500)
        self.get_controller(4, 250)
        self.get_controller(4, 100)
        self.get_controller(8, 100)

    def get_controller(self, frames, interval):
        key = (frames, interval)
        if key in self.controllers.keys():
            return self.controllers[key]
        timer = global_timers.get_timer(interval)
        ctrl = AnimationController(frames_count=frames)
        ctrl.attach_to_timer(timer)
        self.controllers[key] = ctrl
        print(f'Controller {ctrl} created')
        return ctrl


if not GlobalControllers.instance:
    GlobalControllers.instance = GlobalControllers()
global_controllers = GlobalControllers.instance
