import random
from files.content import loader
from core.settings import *
from objects.go import GameObject
from objects import property as p


class PlayerLoader:
    def __init__(self, world):
        # todo asset
        self.world = world

    def load(self, position):
        mock_tileset_data = loader.mock.tileset_data()
        player_sprite = p.SpriteProperty(mock_tileset_data, self.world, position, visible=True,dst_layer=1)

        player_coll = p.CollisionProperty(player_sprite.rect, self.world)
        player_moving = p.MovingProperty(player_coll, self.world)
        player_wsad = p.WSADDriven(player_moving)
        # player_anim_prop = MovementAnimationProperty(player_sprite, player_moving)
        player = GameObject().with_sprite(player_sprite).with_moving(player_moving).with_wsad(
            player_wsad).with_collision(player_coll)
        return player


class TileFactory:
    def __init__(self, map_name, world):
        if map_name not in loader.maps.keys():
            raise ValueError(f"Map {map_name} not in loader {loader.maps.keys()}")
        self.map_name = map_name
        self.world = world

    def new_tile(self, global_index, position):
        # global_index = 91
        if global_index <= 0:
            raise ValueError(f'Tiles indices are > 0, not {global_index}')
        local_index, _, tileset_name, dst = loader.decode_local_index(self.map_name, global_index)
        if global_index > 1:
            print(global_index, ' -> ', local_index, tileset_name)
        tileset_data = loader.tilesets[tileset_name].tileset_data
        # print(global_index, local_index)
        gameobject = GameObject()

        #shilft large objects
        # tile_size_h = tileset_data.tile_size[0]
        # if tile_size_h > TILESIZE:
        position = (position[0] - (tileset_data.tile_size[0] - TILESIZE), position[1] - (tileset_data.tile_size[1] - TILESIZE))


        z_index = len(self.world.get_objects(dst, position))
        print(f"zindex: {z_index}")

        sprite_property = p.SpriteProperty(tileset_data, self.world, position, visible=True, dst_layer=dst, z_index=z_index)
        sprite_property.image_index = local_index
        gameobject.with_sprite(sprite_property)

        # using properties
        tileset_properties = loader.tilesets[tileset_name].tiles_properties
        # print(tileset_properties.keys())
        if local_index in tileset_properties.keys():
            tile_properties = tileset_properties[local_index]
            # print('Yes, ', tile_properties)

            # colllision
            if tile_properties.has_collision_rects():
                for collision_rect in tile_properties.collision_rects:
                    pass  # todo multiple collision rects
                collision_rect = tile_properties.collision_rects[0]
                # print(collision_rect)
                collision_prop = p.CollisionProperty(parent_rect=sprite_property.rect, world=self.world)
                collision_prop.use_fixed_hitbox(collision_rect)
                gameobject.with_collision(collision_prop)

            #animations
            if tile_properties.has_animation():
                for keyframe in tile_properties.animation:
                    pass
                    # print(keyframe)
                # anim_prop = p.AnimationProperty(sprite_property, starting_frame=0, frames_count=4, active=True)
                # anim_prop.attach_own_player(self.world.nature_timer)

            self.world.add_game_object(gameobject, dst)# todo - nie na floor, w map loaderze i stack xy trzeba jakos rozgraniczyc obiekty
        return gameobject

    def build_elevation(self, elevation):
        map_data = loader.maps[self.map_name]
        for idy, stack_row in enumerate(elevation.stack.items):
            for idx, stack_items in enumerate(stack_row):
                for item in stack_items:
                    item_x = idx * map_data.tile_size[0]
                    item_y = idy * map_data.tile_size[1]
                    go = self.new_tile(item, (item_x, item_y))  # todo
                    # self.world.floor.append(go)
                    # print(loader.decode_local_index(self.map_name, item))

    def build_map(self):
        map_data = loader.maps[self.map_name]
        # print(map_data)
        elevation_0 = map_data.elevations[0]
        print(elevation_0)
        self.build_elevation(elevation_0)


class WorldLoader:
    @staticmethod
    def load_test_map(world):
        # todo better but still bad, move out to database
        factory = TileFactory('testmap', world)
        factory.build_map()
