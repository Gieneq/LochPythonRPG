import math
from csv import reader
from os import walk
from time import time_ns

import pygame.image

NEARLY_ZERO = 1e-6


class NanoTimer:
    def __init__(self, init_delta_s=None):
        self.last_time_ns = time_ns()
        self.last_delta_ns = init_delta_s*1e9 if init_delta_s else float(NEARLY_ZERO)

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


def distance_squared(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def radius_squared_from_rect(rect):
    return (rect.w ** 2 + rect.h ** 2) / 4


def distance(p1, p2):
    return math.sqrt(distance_squared(p1, p2))
