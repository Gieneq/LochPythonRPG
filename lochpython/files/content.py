import csv
import os
import pygame
from pygame.rect import Rect
import xml.etree.ElementTree as et
from files.path import ResourceFiles, remove_extension


class TilesetData:
    def __init__(self, name, path, grid_size, tile_size, image_size, with_alpha=True):
        self.name = name
        self.path = path
        self.with_alpha = with_alpha
        surface = pygame.image.load(path)
        self.surface = surface.convert_alpha() if with_alpha else surface.convert()
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.image_size = image_size
        self.tiles_count = self.grid_size[0] * self.grid_size[1]

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

    def column_row_from_local_index(self, index):
        if index >= self.tiles_count:
            raise IndexError(f'Index {index} exceed limit')
        return index % self.columns_count, index // self.columns_count

    def local_index_from_column_row(self, column, row):
        if row * column >= self.tiles_count:
            raise IndexError(f'Index {row * column} exceed limit')
        return row * self.columns_count + column

    def __str__(self):
        return f"Tileset data of {self.name}, grid_size: {self.grid_size}, tile_size: {self.tile_size} with image: {self.surface}"

    @classmethod
    def from_tsx_file(cls, abs_tsx_filepath):
        tileset_node = et.parse(abs_tsx_filepath).getroot()
        tileset_attribs = tileset_node.attrib
        image_attribs = tileset_node.find('image').attrib
        columns_count = int(tileset_attribs['columns'])
        image_abs_path = os.path.join(os.path.dirname(abs_tsx_filepath), image_attribs['source'])

        name = tileset_attribs['name']
        path = image_abs_path
        grid_size = columns_count, int(tileset_attribs['tilecount']) // columns_count
        tile_size = int(tileset_attribs['tilewidth']), int(tileset_attribs['tileheight'])
        image_size = int(image_attribs['width']), int(image_attribs['height'])
        with_alpha = True  # todo

        return cls(name, path, grid_size, tile_size, image_size, with_alpha)


class TileProperties:
    class KeyFrame:
        def __init__(self, tile_id, interval):
            self.tile_id = tile_id
            self.interval = interval

    def __init__(self):
        self.collision_rects = []
        self.animation = []

    def has_animation(self):
        return self.animation

    def has_collision_rects(self):
        return self.collision_rects

    def add_keyframe(self, keyframe):
        if isinstance(keyframe, self.KeyFrame):
            self.animation.append(keyframe)
        else:
            raise ValueError(f"Keyframe should be instance of {self.KeyFrame}")

    def add_collision_rect(self, collision_rect):
        if isinstance(collision_rect, Rect):
            self.animation.append(collision_rect)
        else:
            raise ValueError(f"Collision_rect should be instance of {Rect}")

    def __str__(self):
        return f"Tile properties with collisions: {len(self.collision_rects)}, animations: {len(self.animation)}"

    @classmethod
    def dict_from_tsx_file(cls, abs_tsx_filepath):
        tileset_node = et.parse(abs_tsx_filepath).getroot()

        tiles_data = dict()
        tiles_ids = tileset_node.findall('tile')
        for tile_node in tiles_ids:
            tile_id = int(tile_node.attrib['id'])
            tile_data = TileProperties()

            if collision_groups := tile_node.find('objectgroup'):
                for rect_data in collision_groups:
                    ra = rect_data.attrib
                    rect_position = int(ra['x']), int(ra['y'])
                    rect_size = int(ra['width']), int(ra['height'])
                    tile_data.add_collision_rect(Rect(rect_position, rect_size))

            if animation_node := tile_node.find('animation'):
                for keyframe_data in animation_node:
                    kf_tile_id = int(keyframe_data.attrib['tileid'])
                    kf_interval = int(keyframe_data.attrib['duration'])
                    tile_data.add_keyframe(TileProperties.KeyFrame(kf_tile_id, kf_interval))

            tiles_data[tile_id] = tile_data
        return tiles_data


class Tileset:
    def __init__(self, tileset_data, tiles_properties):
        self.tileset_data = tileset_data
        self.tiles_properties = tiles_properties

    @classmethod
    def from_tsx_file(cls, abs_tsx_filepath):
        return cls(TilesetData.from_tsx_file(abs_tsx_filepath), TileProperties.dict_from_tsx_file(abs_tsx_filepath))

    def __str__(self):
        return f"{self.tileset_data} with properties: \n - " + "\n - ".join(f"{key}: {value}" for key, value in self.tiles_properties.items()) + '\n'



class Loader:
    instance = None

    def __init__(self):
        tilesets_resource_txs_files = ResourceFiles(ResourceFiles.TILESETS).get_tsx_files()
        self.tilesets = dict([(remove_extension(file.name), Tileset.from_tsx_file(file.abs_path)) for file in tilesets_resource_txs_files])
        print(*self.tilesets.values(), sep='\n')

    # def decode_local_index(self, map_name, map_index):
    #     tilesets_ranges = self.maps[map_name]['meta']['index_ranges'].items()
    #     for tileset_name, indices_range in tilesets_ranges:
    #         if map_index in indices_range:
    #             # warning - counting from 1, 0 means missing
    #             local_index = map_index - indices_range.start + 1
    #             return local_index, indices_range, tileset_name
    #     return None

    # def get_tileset(self, tileset_name):
    #     return self.tiles.get(tileset_name, None)

    # def get_tileset_index_data(self, local_index):
    #     return self.tiles.get(tileset_name, None)
    # def get_map_meta(self, tileset_name):
    #     return self.tiles.get(tileset_name, None)


if not Loader.instance:
    Loader.instance = Loader()
loader = Loader.instance






# def load_map(self, file_name, file_path, tiles_data):
#     map_tree = et.parse(file_path)
#     map_tree_root = map_tree.getroot()
#     map_tree_attribs = map_tree_root.attrib
#
#     map_meta = {
#         'name': remove_extension(file_name),
#         'path': file_path,
#         'grid_size': (int(map_tree_attribs['width']), int(map_tree_attribs['height'])),
#         'tile_size': (int(map_tree_attribs['tilewidth']), int(map_tree_attribs['tileheight'])),
#     }
#
#     # tilesets - moze przyspieszy wyszukiwanie ale niekoniecznie
#     tilesets_index_ranges = dict()
#     map_tileset_nodes = map_tree_root.findall('tileset')  # needs info about tilesets
#     for map_tileset_node in map_tileset_nodes:
#         tileset_attribs = map_tileset_node.attrib
#         tileset_fgid = int(tileset_attribs['firstgid'])
#         tilset_name = tileset_attribs['source'].strip().split('/')[-1].split('.')[0]
#         if tilset_name in tiles_data:
#             grid_size = tiles_data[tilset_name]['grid_size']
#             tiles_count = grid_size[0] * grid_size[1]
#             print(tiles_data[tilset_name])
#             tilesets_index_ranges[tilset_name] = range(tileset_fgid, tileset_fgid + tiles_count)
#         else:
#             raise FileNotFoundError('Missing tileset file:', tilset_name)
#     map_meta['index_ranges'] = tilesets_index_ranges
#
#     # groups
#     map_group_nodes = map_tree_root.findall('group')
#     # print(map_group_nodes)
#
#     map_data = [0] * len(map_group_nodes)
#
#     for map_group_node in map_group_nodes:
#         elevation_index = int(map_group_node.attrib['name'].split('_')[1])
#         # print('Elevation:', elevation_index)
#         layers = map_group_node.findall('layer')
#         layers_stack = [None] * len(layers)
#
#         for layer in layers:
#             # print(layer)
#             layer_index = int(layer.attrib['name'].split('_')[0])
#             layer_csv_raw = layer.findall('data')[0]
#             layer_csv = list(csv.reader(layer_csv_raw.text.strip().split('\n')))
#             # layer_csv = [int(item) for row in layer_csv for item in row if item]
#             layer_csv = [[int(item) for item in row if item] for row in layer_csv]
#             layers_stack[layer_index] = layer_csv
#         # print(*layers_stack)
#         map_data[elevation_index] = layers_stack
#     return {
#         'meta': map_meta,
#         'data': map_data
#     }
#
#
# def __init__(self, tiles_data):
#     print('Loading maps data')
#     self.maps = dict()
#     for filename, path in get_resource_abs_path(MAPS_PATH):
#         self.maps[remove_extension(filename)] = self.load_map(filename, path, tiles_data)
#     # print(*maps.items(), sep='\n')
#     print(self.maps['testmap']['meta'])
