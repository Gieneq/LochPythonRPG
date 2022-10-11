from csv import reader
from os import walk
from time import time_ns

import pygame.image

NEARLY_ZERO = 1e-6


class NanoTimer:
    def __init__(self):
        self.last_time_ns = 0
        self.last_delta_ns = float(NEARLY_ZERO)

    @staticmethod
    def ns_to_s(ns):
        return ns / float(1e9)

    def start(self):
        self.last_delta_ns = self.delta_time_ns
        self.last_time_ns = time_ns()

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


def import_csv_layout(path):
    with open(path) as file:
        terrain_map = []
        layout = reader(file, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surfaces_list = []
    for _, __, img_filenames in walk(path):
        for img_filename in img_filenames:
            img_path = path + '/' + img_filename
            img_surf = pygame.image.load(img_path).convert_alpha()
            surfaces_list.append(img_surf)
    return surfaces_list
