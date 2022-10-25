import os
from functools import reduce

import pygame
from core.settings import GRAPHICS_TILESETS_PATHS, GRAPHICS_ENTITIES_PATHS, MAPS_PATH
from itertools import chain
import xml.etree.ElementTree as et

from files.path import get_resource_abs_path, filter_path_by_type


class ImageMeta:
    def __init__(self, name_id, path, image, grid_size=(1, 1)):
        self.name_id = name_id
        self.image = image
        self.path = path
        self.tile_size = (image.get_width() / grid_size[0], image.get_height() / grid_size[1])
        self.grid_size = grid_size

    @property
    def columns_count(self):
        return self.grid_size[0]

    @property
    def rows_count(self):
        return self.grid_size[1]

    @property
    def tile_width(self):
        return self.tile_size[0]

    @property
    def tile_height(self):
        return self.tile_size[1]

    def column_row_from_index(self, index):
        return index % self.columns_count, index // self.columns_count

    def index_from_column_row(self, column, row):
        return row * self.columns_count + column

    def __str__(self):
        return f"Image meta of {self.name_id}, grid: {self.grid_size}, tsize: {self.tile_size}"


class ImagesLoader:
    instance = None

    def get_map_data(self, map_dir_path):
        print('Extracting', map_dir_path)
        _, map_dirs = get_resource_abs_path(map_dir_path)
        some_dir = list(map_dirs)[0]
        content_filenames, content_paths = get_resource_abs_path(some_dir)
        print(*content_paths)
        print(*content_filenames)

    def meta_from_image(self, tsx_filepath):
        tsx_tree = et.parse(tsx_filepath)
        tileset_node = tsx_tree.getroot()
        tileset_attribs = tileset_node.attrib
        image_attribs = [*tileset_node][0].attrib
        columns_count = int(tileset_attribs['columns'])

        meta = {
            'source_image': os.path.join(GRAPHICS_TILESETS_PATHS, image_attribs['source']),
            'tile_width': int(tileset_attribs['tilewidth']),
            'tile_height': int(tileset_attribs['tileheight']),
            'grid_columns': columns_count,
            'grid_rows': int(tileset_attribs['tilecount']) // columns_count,
            'image_width': int(image_attribs['width']),
            'image_height': int(image_attribs['height']),
        }
        return tileset_attribs['name'], meta

    def get_graphics_meta(self, path):
        paths = list(get_resource_abs_path(path)[1])
        image_paths = [*filter_path_by_type(paths, 'png')]
        meta_paths = [*filter_path_by_type(paths, 'tsx')]
        if len(image_paths) != len(meta_paths):
            raise FileNotFoundError(f'Some resources files are missing in {path}')
        return dict(map(lambda p: self.meta_from_image(p), meta_paths))

    def __init__(self):
        graphics_meta = {
            'tilesets': self.get_graphics_meta(GRAPHICS_TILESETS_PATHS),
            'entities': self.get_graphics_meta(GRAPHICS_ENTITIES_PATHS)
        }
        print(graphics_meta)

        maps_da = self.get_map_data(MAPS_PATH)

    def _load_image(cls, path, name_id, grid_size=(1, 1), with_alpha=True):
        image = pygame.image.load(path).convert_alpha()  # todo
        return ImageMeta(name_id=name_id, path=path, image=image, grid_size=grid_size)


if not ImagesLoader.instance:
    ImagesLoader.instance = ImagesLoader()
loader = ImagesLoader.instance
