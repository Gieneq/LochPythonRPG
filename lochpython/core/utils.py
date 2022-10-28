import math
from time import time_ns

from pygame.rect import Rect

NEARLY_ZERO = 1e-6


class StackXY:
    def __init__(self, width, height, initial=None):
        self.width, self.height = width, height

        self.items = []
        for index_y in range(height):
            row = []
            for index_x in range(width):
                row.append([])
            self.items.append(row)

    def get_stack(self, x, y):
        return self.items[y][x]

    def get_top_stack(self, x, y):
        stack = self.get_stack(x, y)
        if stack:
            return stack[-1]
        return None

    def get_bottom_stack(self, x, y):
        stack = self.get_stack(x, y)
        if stack:
            return stack[0]
        return None

    def push_top(self, x, y, value):
        self.get_stack(x, y).append(value)

    def pop_top(self, x, y):
        stack = self.get_stack(x, y)
        if stack:
            return stack.pop()
        return None

    def __str__(self):
        return f"StackXY ({self.width} x {self.height})."

    def print_stack_counts(self, indentation):
        lines = ''
        for stack_row in self.items:
            lines += indentation + ', '.join([str(len(field)) for field in stack_row]) + ',\n'
        return lines
    def print_stack(self, indentation):
        lines = ''
        for stack_row in self.items:
            lines += indentation + ', '.join([str(field) for field in stack_row]) + ',\n'
        return lines


class NanoTimer:
    def __init__(self, init_delta_s=None):
        self.last_time_ns = time_ns()
        self.last_delta_ns = init_delta_s * 1e9 if init_delta_s else float(NEARLY_ZERO)

    @staticmethod
    def ns_to_s(ns):
        return ns / float(1e9)

    def start(self):
        self.last_delta_ns = self.delta_time_ns
        self.last_time_ns = time_ns()
        return self

    @property
    def delta_time_ns(self):
        return time_ns() - self.last_time_ns

    @property
    def delta_time_s(self):
        return NanoTimer.ns_to_s(self.delta_time_ns)

    @property
    def last_time_s(self):
        return NanoTimer.ns_to_s(self.last_time_ns)

    @property
    def last_delta_s(self):
        return NanoTimer.ns_to_s(self.last_delta_ns)


def sub_tuples_2D(t1, t2):
    return t1[0] - t2[0], t1[1] - t2[1]
def add_tuples_2D(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]


def distance_squared(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def radius_squared_from_rect(rect):
    return (rect.w ** 2 + rect.h ** 2) / 4


def distance(p1, p2):
    return math.sqrt(distance_squared(p1, p2))


class ValueFilter:
    def __init__(self, size=16):
        self.buffer = [0] * size
        self.idx = 0

    def push_value(self, v):
        self.buffer[self.idx] = v
        self.idx = (self.idx + 1) % len(self.buffer)

    @property
    def average(self):
        return sum(self.buffer) / len(self.buffer)

    @property
    def median(self):
        return sorted(self.buffer)[len(self.buffer) // 2]

    def __str__(self):
        return str(self.average)


def is_container(value):
    for options in (list, dict, tuple):
        if isinstance(value, options):
            return True
    return False


def nested_print(data, indent=0, tab=' '):
    if isinstance(data, dict):
        print(tab * indent + '{')
        for key, value in data.items():
            print(tab * indent + str(key), end=': ')
            nested_print(value, indent + 1)
        print(tab * indent + '}')

    elif isinstance(data, list) or isinstance(data, tuple):
        print(tab * indent + '[')
        for value in data:
            nested_print(value, indent + 1)
        print(tab * indent + ']')
    else:
        print(tab * indent + str(data))


def generate_span_rect(rects):
    result = Rect(rects[0])
    if len(rects) == 1:
        return result
    for rect in rects[1:]:
        right = max(result.right, rect.right)
        bottom = max(result.bottom, rect.bottom)
        result.left = min(result.left, rect.left)
        result.top = min(result.top, rect.top)
        result.w = abs(right - result.left)
        result.h = abs(bottom - result.top)
    return result