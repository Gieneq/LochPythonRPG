import random
from files.content import loader
from core.settings import *
from objects.go import GameObject
from objects import property as p
from core.timers import global_controllers


class PlayerLoader:
    def __init__(self, world):
        # todo asset
        self.world = world

    def load(self, position):
        mock_tileset_data = loader.mock.tileset_data()
        # mock_tileset_data.surface.set_colorkey((255,0,255)) #todo lol
        player_sprite = p.SpriteProperty(mock_tileset_data, self.world, position, visible=True, dst_layer=1)  # todo

        player_coll = p.CollisionProperty(player_sprite.rect, self.world)
        player_moving = p.MovingProperty(player_coll, self.world)
        player_wsad = p.WSADDriven(player_moving)

        prts_tileset = loader.tilesets['particles']
        print(prts_tileset)
        prts_tileset_data = loader.tilesets['particles'].tileset_data
        print(prts_tileset_data)
        prts_tileset_props = loader.tilesets['particles'].tiles_properties
        print(*prts_tileset_props.values())


        # todo zbuduj zestaw



        particle_data = loader.mock.tileset_data()
        particle_sprite = p.SpriteProperty(prts_tileset_data, self.world, position, visible=True, dst_layer=1)

        player_as_emiter = p.EmitterProperty(particle_sprite)
        # player_anim_prop = p.MovementAnimationProperty(player_sprite, player_moving)
        player = GameObject().with_sprite(player_sprite).with_moving(player_moving).with_wsad(
            player_wsad).with_collision(player_coll).with_emitter(player_as_emiter)
        return player


class TileFactory:
    def __init__(self, map_name, world):
        if map_name not in loader.maps.keys():
            raise ValueError(f"Map {map_name} not in loader {loader.maps.keys()}")
        self.map_name = map_name
        self.world = world

    def new_tile(self, global_index, position):
        if global_index <= 0:
            raise ValueError(f'Tiles indices are > 0, not {global_index}')
        local_index, _, tileset_name, dst = loader.decode_local_index(self.map_name, global_index)
        # if global_index > 1:
        #     print(global_index, ' -> ', local_index, tileset_name)
        tileset_data = loader.tilesets[tileset_name].tileset_data
        gameobject = GameObject()

        # shilft large objects
        pos_x = position[0]  # - (tileset_data.tile_size[0] - TILESIZE)
        pos_y = position[1] - (tileset_data.tile_size[1] - TILESIZE)
        position = (pos_x, pos_y)

        z_index = len(self.world.get_objects(dst, position))
        # print(f"zindex: {z_index}")

        sprite_property = p.SpriteProperty(tileset_data, self.world, position, visible=True, dst_layer=dst,
                                           z_index=z_index)
        sprite_property.image_index = local_index
        gameobject.with_sprite(sprite_property)

        # using properties
        tileset_properties = loader.tilesets[tileset_name].tiles_properties
        if local_index in tileset_properties.keys():
            tile_properties = tileset_properties[local_index]

            # colllision
            if tile_properties.has_collision_rects():
                collision_prop = p.CollisionProperty(parent_rect=sprite_property.rect, world=self.world)
                collision_prop.add_hitboxes(tile_properties.collision_rects)
                gameobject.with_collision(collision_prop)

            # animations
            if tile_properties.has_animation():
                anim_prop = p.AnimationProperty(sprite_property)
                animation_frames = tile_properties.animation
                frames_count = len(animation_frames)
                frames_interval = animation_frames[0].interval
                for keyframe in animation_frames:
                    anim_prop.keyframes.append(keyframe)
                anim_prop.active = True
                anim_prop.attach_to_controller(global_controllers.get_controller(frames_count, frames_interval))
                gameobject.with_animation(anim_prop)  # todo

            # light
            if tile_properties.has_light_effect():
                le = tile_properties.light_effect
                light_prop = p.LightSourceProperty(sprite_property.rect, le.relative_position, le.strength, le.color, le.active)
                gameobject.with_light_source(light_prop)

            self.world.add_game_object(gameobject, dst)
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
