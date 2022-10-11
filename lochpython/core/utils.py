from csv import reader
from os import walk

import pygame.image


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
