import csv
import os
from functools import reduce

import pygame
from pygame.rect import Rect

from core.settings import GRAPHICS_TILESETS_PATHS, GRAPHICS_ENTITIES_PATHS, MAPS_PATH
from itertools import chain
import xml.etree.ElementTree as et

from core.utils import StackXY
from files.path import get_resource_abs_path, filter_path_by_type, remove_extension


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


class TilesetLoader:

    def image_meta_from_tsx(self, tsx_filepath):
        tsx_tree = et.parse(tsx_filepath)
        tileset_node = tsx_tree.getroot()
        tileset_attribs = tileset_node.attrib
        image_attribs = [*tileset_node][0].attrib
        columns_count = int(tileset_attribs['columns'])

        image_meta = {
            'source_image': os.path.join(GRAPHICS_TILESETS_PATHS, image_attribs['source']),
            'tile_width': int(tileset_attribs['tilewidth']),
            'tile_height': int(tileset_attribs['tileheight']),
            'grid_columns': columns_count,
            'grid_rows': int(tileset_attribs['tilecount']) // columns_count,
            'image_width': int(image_attribs['width']),
            'image_height': int(image_attribs['height']),
        }
        image_data = {}
        tile_ids = tileset_node.findall('tile')
        for tile_id in tile_ids:
            tile_data = {}

            if collision_groups_raw := tile_id.find('objectgroup'):
                collision_rects = []
                for rect_raw in collision_groups_raw:
                    ra = rect_raw.attrib
                    point = int(ra['x']), int(ra['y'])
                    size = int(ra['width']), int(ra['height'])
                    collision_rects.append(Rect(point, size))
                tile_data['collisions'] = collision_rects,

            if animation_node := tile_id.find('animation'):
                animation_data = []
                for frame in animation_node:
                    animation_data.append({
                        'tile_id':int(frame.attrib['tileid']),
                        'interval':int(frame.attrib['duration']),
                    })
                tile_data['animation'] = animation_data,

            image_data[int(tile_id.attrib['id'])] = tile_data
        image_meta['data'] = image_data

        result = tileset_attribs['name'], image_meta
        print(result[0])
        print(*[r for r in result[1].items() if r[0] != 'data'], sep='\n')
        print(*result[1]['data'].items(), sep='\n')
        return result

    def get_graphics_meta(self, path):
        paths = get_resource_abs_path(path)
        image_paths = [*filter_path_by_type(paths, 'png')]
        meta_paths = [*filter_path_by_type(paths, 'tsx')]
        if len(image_paths) != len(meta_paths):
            raise FileNotFoundError(f'Some resources files are missing in {path}')
        return dict(map(lambda p: self.image_meta_from_tsx(p[1]), meta_paths))

    def __init__(self):
        tileset_info = self.get_graphics_meta(GRAPHICS_TILESETS_PATHS)
        # print(*tileset_info.items(), sep='\n')


class MapLoader:

    def load_map(self, file_name, file_path):
        map_tree = et.parse(file_path)
        map_tree_root = map_tree.getroot()
        map_tree_attribs = map_tree_root.attrib

        map_meta = {
            'name': remove_extension(file_name),
            'path': file_path,
            'grid_size': (int(map_tree_attribs['width']), int(map_tree_attribs['height'])),
            'tile_size': (int(map_tree_attribs['tilewidth']), int(map_tree_attribs['tileheight'])),
        }
        # print(map_meta)

        # tilesets - moze przyspieszy wyszukiwanie ale niekoniecznie
        map_tileset_nodes = map_tree_root.findall('tileset')  # needs info about tilesets
        # print(map_tileset_nodes)

        # groups
        map_group_nodes = map_tree_root.findall('group')
        # print(map_group_nodes)

        map_data = [0] * len(map_group_nodes)

        for map_group_node in map_group_nodes:
            elevation_index = int(map_group_node.attrib['name'].split('_')[1])
            # print('Elevation:', elevation_index)
            layers = map_group_node.findall('layer')
            layers_stack = [None] * len(layers)

            for layer in layers:
                # print(layer)
                layer_index = int(layer.attrib['name'].split('_')[0])
                layer_csv_raw = layer.findall('data')[0]
                layer_csv = list(csv.reader(layer_csv_raw.text.strip().split('\n')))
                # layer_csv = [int(item) for row in layer_csv for item in row if item]
                layer_csv = [[int(item) for item in row if item] for row in layer_csv]
                layers_stack[layer_index] = layer_csv
            # print(*layers_stack)
            map_data[elevation_index] = layers_stack
        return {
            'meta': map_meta,
            'data': map_data
        }

    def __init__(self):
        maps = dict()
        for filename, path in get_resource_abs_path(MAPS_PATH):
            maps[remove_extension(filename)] = self.load_map(filename, path)
        # print(*maps.items(), sep='\n')
        print(maps['testmap']['meta'])


class Loader:
    instance = None

    def __init__(self):
        print('MAP')
        MapLoader()
        print()
        print('TILES')
        TilesetLoader()
        print()

    def _load_image(cls, path, name_id, grid_size=(1, 1), with_alpha=True):
        image = pygame.image.load(path).convert_alpha()  # todo
        return ImageMeta(name_id=name_id, path=path, image=image, grid_size=grid_size)


if not Loader.instance:
    Loader.instance = Loader()
loader = Loader.instance
