from core.settings import *


class Debugger:
    debug_lines = []
    rects = []

    @classmethod
    def print(cls, *objects, sep=', '):
        if DEBUG:
            cls.debug_lines.append(sep.join([str(obj) for obj in objects]))

    @classmethod
    def rect(cls, rect, color, border=1):
        if DEBUG:
            cls.rects.append((rect, color, border))

    @classmethod
    def clear_rects(cls):
        cls.rects.clear()

    @classmethod
    def clear_gui(cls):
        cls.debug_lines.clear()
