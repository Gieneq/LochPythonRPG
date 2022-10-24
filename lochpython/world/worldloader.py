import random

from core.settings import *
from objects.go import GameObject
from objects.property import Props, SpriteProperty, CollisionProperty, MovingProperty, WSADDriven, AnimationProperty, \
    MovementAnimationProperty, AnimationPlayer


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

    @classmethod
    def load_image(cls, path, name_id, grid_size=(1, 1), with_alpha=True):
        image = pygame.image.load(path).convert_alpha()  # todo
        return cls(name_id=name_id, path=path, image=image, grid_size=grid_size)

    def __str__(self):
        return f"Image meta of {self.name_id}, grid: {self.grid_size}, tsize: {self.tile_size}"


class ImagesLoader:
    instance = None

    def __init__(self):
        self.floor_image = ImageMeta.load_image('./data/tilesets/floor.png', 'floor', (15, 15))
        self.details_image = ImageMeta.load_image('./data/tilesets/details.png', 'details', (15, 15))
        self.objects_image = ImageMeta.load_image('./data/tilesets/objects.png', 'objects_1x1', (15, 15))
        self.objects_1x2_image = ImageMeta.load_image('./data/tilesets/objects_1x2.png', 'objects_1x2', (15, 7.5))
        self.player_image = ImageMeta.load_image('./data/entities/player.png', 'player', (12, 4))
        # todo load info about tileset
        # todo player animations etc


if not ImagesLoader.instance:
    ImagesLoader.instance = ImagesLoader()
loader = ImagesLoader.instance


class WorldLoader:
    @staticmethod
    def load_csv_map(path):
        with open(path, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]

    # def import_folder(path):
    #     surfaces_list = []
    #     for _, __, img_filenames in walk(path):
    #         for img_filename in img_filenames:
    #             img_path = path + '/' + img_filename
    #             img_surf = pygame.image.load(img_path).convert_alpha()
    #             surfaces_list.append(img_surf)
    #     return surfaces_list
    @staticmethod
    def build_water_tile(world, position, idx=0):
        floor_tile = GameObject()

        image = loader.floor_image
        sprite_prop = SpriteProperty(image, world, position, visible=True, stack_layer=SpriteProperty.Layer.FLOOR)
        sprite_prop.image_index = idx
        floor_tile.with_sprite(sprite_prop)  # todo not repeat, add some common data for static tiles
        frames_c = world.nature_timer.frames_count
        water_anim_prop = AnimationProperty(sprite_prop, frames_count=frames_c, active=True, starting_frame=idx)
        # water_anim_prop.attach_own_player(world.nature_timer)
        world.nature_timer.handlers.append(water_anim_prop.next_frame)
        floor_tile.with_animation(water_anim_prop)
        return floor_tile

    @staticmethod
    def load_test_map(world):
        # todo better but still bad, move out to database

        floor_data = WorldLoader.load_csv_map('./data/maps/TheLoch/theloch._Floor_0_base.csv')
        # details_lower_data = WorldLoader.load_csv_map('./data/maps/TheLoch/map_first._Details_Details_lower.csv')
        # details_upper_data = WorldLoader.load_csv_map('./data/maps/TheLoch/map_first._Details_Details_upper.csv')
        # objects_1x1_data = WorldLoader.load_csv_map('./data/maps/TheLoch/map_first._Details_Objects_1x1.csv')
        # objects_1x2_data = WorldLoader.load_csv_map('./data/maps/TheLoch/map_first._Details_Objects_1x2.csv')
        # limit_data = WorldLoader.load_csv_map('./data/maps/TheLoch/map_first._Details_Limits.csv')

        player_sprite = SpriteProperty(loader.player_image, world, (1214, 1233), visible=True,
                                       stack_layer=SpriteProperty.Layer.OBJECTS)
        player_coll = CollisionProperty(player_sprite.rect, world)
        player_moving = MovingProperty(player_coll, world)
        player_wsad = WSADDriven(player_moving)
        player_anim_prop = MovementAnimationProperty(player_sprite, player_moving)
        player = GameObject().with_sprite(player_sprite).with_moving(player_moving).with_wsad(
            player_wsad).with_collision(player_coll).with_animation(player_anim_prop)
        world.entities.append(player)
        world.player = player

        # floor
        for row_idx, row in enumerate(floor_data):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                idx = int(col)
                if idx % 15 == 0:
                    floor_tile = WorldLoader.build_water_tile(world, (x, y), idx)
                else:
                    floor_tile = GameObject()
                    sprite_prop = SpriteProperty(loader.floor_image, world, (x, y), visible=True,
                                                 stack_layer=SpriteProperty.Layer.DETAILS)
                    sprite_prop.image_index = idx
                    floor_tile.with_sprite(sprite_prop)

                # todo indicate tile is animated, some need for metadata 😒

                world.floor.append(floor_tile)

        # # details
        # details_levels = [details_lower_data, details_upper_data]
        # for detail_level in details_levels:
        #     for row_idx, row in enumerate(detail_level):
        #         for col_idx, col in enumerate(row):
        #             x = col_idx * TILESIZE
        #             y = row_idx * TILESIZE
        #             idx = int(col)
        #             if idx == -1:
        #                 continue
        #             detail_tile = GameObject()
        #             image_meta = loader.details_image
        #             sprite_prop = SpriteProperty(image_meta, world, (x, y), visible=True,
        #                                          stack_layer=SpriteProperty.Layer.DETAILS)
        #             sprite_prop.image_index = idx
        #             detail_tile.with_sprite(sprite_prop)
        #             if idx == 11 or idx == 13:
        #                 anim_prop = AnimationProperty(sprite_prop, active=True, starting_frame=idx, frames_count=2)
        #                 world.nature_timer.handlers.append(anim_prop.next_frame)
        #
        #                 # anim_prop.attach_own_player(AnimationPlayer(anim_prop.frames_count, duration=8))
        #                 detail_tile.with_animation(anim_prop)
        #
        #             world.floor_details.append(detail_tile)
        #
        #
        # # objects 1x1
        # for row_idx, row in enumerate(objects_1x1_data):
        #     for col_idx, col in enumerate(row):
        #         x = col_idx * TILESIZE
        #         y = row_idx * TILESIZE
        #         idx = int(col)
        #         if idx > -1:
        #             image = loader.objects_image
        #             object_tile = GameObject()
        #             sprite_prop = SpriteProperty(image, world, (x, y), visible=True,
        #                                          stack_layer=SpriteProperty.Layer.DETAILS)
        #             sprite_prop.image_index = idx
        #             collide_prop = CollisionProperty(sprite_prop.rect, world)
        #             object_tile.with_sprite(sprite_prop).with_collision(collide_prop)
        #
        #             if idx in [2,6]:
        #                 sprite_prop.image_index = idx + random.randint(0,4)
        #
        #             if idx in [15]:
        #                 anim_prop = AnimationProperty(sprite_prop, active=True, starting_frame=idx, frames_count=2)
        #                 # anim_prop.attach_own_player(world.nature_timer)
        #                 world.nature_timer.handlers.append(anim_prop.next_frame)
        #                 object_tile.with_animation(anim_prop)
        #
        #
        #             world.entities.append(object_tile)
        #
        #
        # # objects 1x2
        # for row_idx, row in enumerate(objects_1x2_data):
        #     for col_idx, col in enumerate(row):
        #         x = col_idx * TILESIZE
        #         y = (row_idx-1) * TILESIZE
        #         idx = int(col)
        #         if idx > -1:
        #             image = loader.objects_1x2_image
        #             object_tile = GameObject()
        #             sprite_prop = SpriteProperty(image, world, (x, y), visible=True,
        #                                          stack_layer=SpriteProperty.Layer.OBJECTS)
        #             sprite_prop.image_index = idx
        #             collide_prop = CollisionProperty(sprite_prop.rect, world)
        #             object_tile.with_sprite(sprite_prop).with_collision(collide_prop)
        #
        #             world.entities.append(object_tile)
        # # return
        # # limits
        # for row_idx, row in enumerate(limit_data):
        #     for col_idx, col in enumerate(row):
        #         x = col_idx * TILESIZE
        #         y = row_idx * TILESIZE
        #         if col != '-1':
        #             limit_rect = pygame.Rect((x, y), (TILESIZE, TILESIZE))
        #             limit_block = GameObject().with_collision(CollisionProperty(limit_rect, world))
        #             world.limit_blocks.append(limit_block)
