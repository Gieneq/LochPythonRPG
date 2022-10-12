from core.settings import *


class Debugger:
    debug_lines = []

    @classmethod
    def print(cls, *objects, sep=', '):
        if DEBUG:
            cls.debug_lines.append(sep.join([str(obj) for obj in objects]))

    @classmethod
    def clear(cls):
        cls.debug_lines.clear()
