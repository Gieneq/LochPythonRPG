from core.settings import TILESIZE
import os
import pygame
from pygame.rect import Rect
import xml.etree.ElementTree as et

from core.utils import StackXY
from files.path import ResourceFiles, remove_extension
from objects.go import GameObject


class TilesetData:
    def __init__(self, name, path, grid_size, tile_size, image_size, with_alpha=True):
        self.name = name
        self.path = path
        self.with_alpha = with_alpha
        if path:
            surface = pygame.image.load(path)
            self.surface = surface.convert_alpha() if with_alpha else surface.convert()
        else:
            self.surface = pygame.Surface(image_size)
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.image_size = image_size
        self.tiles_count = self.grid_size[0] * self.grid_size[1]

    def set_color(self, color):
        self.surface.fill(color)

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
            self.collision_rects.append(collision_rect)
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
        return f"{self.tileset_data} with properties: \n - " + "\n - ".join(
            f"{key}: {value}" for key, value in self.tiles_properties.items()) + '\n'


class RegionMap:
    class Elevation:
        def __init__(self, name, width, height):
            self.name = name
            self.stack = StackXY(width, height, initial=0)

        def __str__(self):
            return f"Elevation {self.name}: {self.stack}. Stacked counts: \n{self.stack.print_stack(indentation='  ' * 2)}"

    def __init__(self, path, map_size, tile_size):
        self.path = path
        self.map_size = map_size
        self.tile_size = tile_size
        self.global_ids = dict()
        self.elevations = []

    def add_global_id(self, tileset_name, ids_range):
        self.global_ids[tileset_name] = ids_range

    def setup_elevations(self, count):
        self.elevations = [None] * count

    def add_elevation(self, elevation_idx, elevation: Elevation):
        self.elevations[elevation_idx] = elevation

    def __str__(self):
        lines = f"RegionMap {self.path} with {len(self.elevations)} elevations. Size {self.map_size}, used GIDS: \n - "
        lines += '\n - '.join(f"{name}: {gids_range}" for name, gids_range in self.global_ids.items()) + '\n'
        lines += f"Elevations {len(self.elevations)}: \n - "
        lines += '\n - '.join(f"{idx}: {e}" for idx, e in enumerate(self.elevations))
        return lines

    @classmethod
    def from_tsx_file(cls, abs_tmx_filepath, tilesets):
        print(abs_tmx_filepath)
        map_node = et.parse(abs_tmx_filepath).getroot()
        map_attribs = map_node.attrib
        path = abs_tmx_filepath
        map_size = (int(map_attribs['width']), int(map_attribs['height']))
        tile_size = (int(map_attribs['tilewidth']), int(map_attribs['tileheight']))
        print(path)

        region_map = cls(path, map_size, tile_size)

        for tileset_gid_node in map_node.findall('tileset'):
            gid_attribs = tileset_gid_node.attrib
            tileset_name = remove_extension(gid_attribs['source'].split('/')[-1])
            gid_start = int(gid_attribs['firstgid'])
            gid_range = range(gid_start, tilesets.get(tileset_name).tileset_data.tiles_count + gid_start)
            region_map.add_global_id(tileset_name, gid_range)

        # elevation is stack of layers - flatten group
        elevations = map_node.findall('group')

        region_map.setup_elevations(len(elevations))
        for elevation_node in elevations:
            elevation_name = elevation_node.attrib['name']
            elevation_idx = int(elevation_name.strip().split('_')[0])
            elevation = cls.Elevation(elevation_name, *region_map.map_size)
            region_map.add_elevation(elevation_idx, elevation)

            layers_nodes = [(int(layer.attrib['name'].split('_')[0]), layer) for layer in
                            elevation_node.findall('layer')]
            layers_nodes.sort(key=lambda x: x[0])
            for idx, layer in layers_nodes:
                layer_csv_rows = layer.find('data').text.strip().split(',\n')
                for index_y, csv_row in enumerate(layer_csv_rows):
                    items = list(int(item) for item in csv_row.strip().split(','))
                    for index_x, item in enumerate(items):
                        if item > 0:
                            elevation.stack.push_top(index_x, index_y, item)
            # print(elevation)

        return region_map


class Mock:
    index = 0
    @staticmethod
    def tileset_data(color=(255, 0, 255)):
        grid_size = (1, 1)
        tile_size = (TILESIZE, TILESIZE)
        image_size = grid_size[0] * tile_size[0], grid_size[1] * tile_size[1]
        tileset_data = TilesetData(f'mock_{Mock.index}', None, grid_size, tile_size, image_size, with_alpha=False)
        tileset_data.set_color(color)
        Mock.index += 1
        return tileset_data


class Loader:
    """
    Tileset resources:
     loader.tilset.get('floor').tileset_data.tile_size # name, path, with_alpha, surface, tile_size, grid_size, image_size, tiles_count
     loader.tilset.get('floor').tileset_properties.get(0).animation # collision_rects
    """
    instance = None

    def __init__(self):
        tilesets_resource_txs_files = ResourceFiles(ResourceFiles.TILESETS).get_tsx_files()
        self.tilesets = dict([(remove_extension(file.name), Tileset.from_tsx_file(file.abs_path)) for file in
                              tilesets_resource_txs_files])

        maps_resource_tms_files = ResourceFiles(ResourceFiles.MAPS).get_tmx_files()
        print(maps_resource_tms_files[0].abs_path)
        self.maps = dict(
            [(remove_extension(file.name), RegionMap.from_tsx_file(file.abs_path, self.tilesets)) for file in
             maps_resource_tms_files])

        self.mock = Mock
        # for region_map_name, region_map_data in self.maps.items():
        #     print(region_map_name, region_map_data)

        # print(self.decode_local_index('testmap', 450))

    def decode_local_index(self, map_name, map_index):
        map_ragion = self.maps.get(map_name)
        if not map_ragion:
            raise FileNotFoundError(f"Missing map {map_name}")

        for tileset_name, indices_range in map_ragion.global_ids.items():
            if map_index in indices_range:
                # be aware - counting from 1, 0 means missing
                local_index = map_index - indices_range.start  # + 1
                # if local_index < 0:
                #

                mock_destination = 0
                # if tileset_name == 'floor' or tileset_name == 'details':
                #     mock_destination = GameObject.GOType.BASEMENT
                if tileset_name.startswith('objects'):
                    mock_destination = 1
                return local_index, indices_range, tileset_name, mock_destination
        return None


if not Loader.instance:
    Loader.instance = Loader()
loader = Loader.instance
