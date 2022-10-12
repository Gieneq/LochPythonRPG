import pygame

from entity.player import Player


class World:
    def __init__(self):
        # cls.visible_sprites = pygame.sprite.Group()#YSortCameraGroup()
        # cls.obstacle_sprites = pygame.sprite.Group()
        self.visible_objects = pygame.sprite.Group()
        self.obstacle_objects = pygame.sprite.Group()

        # self.player = Player((757, 1242), (self.visible_objects, ), self.obstacle_objects)

        self.player = Player((50, 70), (self.visible_objects,))

    def add_entity(self, entity):
        pass

    def update(self, dt):
        self.visible_objects.update(dt=dt)

# class YSortCameraGroup(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__()
#         self.display_surface = pygame.display.get_surface()
#         self.half_width = self.display_surface.get_width() // 2
#         self.half_height = self.display_surface.get_height() // 2
#         self.offset = pygame.math.Vector2()
#
#         self.floor_surf = pygame.image.load('./data/graphics/tilemap/ground.png')
#         self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
#
#     def custom_draw(self, player):
#         # getting the offset
#         self.offset.x = player.rect.centerx - self.half_width
#         self.offset.y = player.rect.centery - self.half_height
#
#         offset_position = self.floor_rect.topleft - self.offset
#         self.display_surface.blit(self.floor_surf, offset_position)
#
#         for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
#             offset_position = sprite.rect.topleft - self.offset
#             self.display_surface.blit(sprite.image, offset_position)


# class Level:
#     def __init__(self):
#
#         # get display furface
#
#         # sprites groups setup
#
#         # map setup
#         self.create_map()
#
#     def create_map(self):
#         # layout = {
#         #     'boundary': import_csv_layout('../../data/map/map_FloorBlocks.csv'),
#         #     'grass': import_csv_layout('../../data/map/map_Grass.csv'),
#         #     'object': import_csv_layout('../../data/map/map_LargeObjects.csv'),
#         # }
#         #
#         # graphics = {
#         #     'grass': import_folder('../../data/graphics/grass'),
#         #     'object': import_folder('../../data/graphics/objects'),
#         # }
#         #
#         # for style, layout in layout.items():
#         #     for row_idx, row in enumerate(layout):
#         #         for col_idx, col in enumerate(row):
#         #             if col != '-1':
#         #                 x = col_idx * TILESIZE
#         #                 y = row_idx * TILESIZE
#         #                 if style == 'boundary':
#         #                     Tile((x, y), [self.obstacle_sprites], sprite_type='invisible')
#         #                 if style == 'grass':
#         #                     grass_surface = random.choice(graphics['grass'])
#         #                     Tile((x, y), [self.visible_sprites, self.obstacle_sprites], sprite_type='grass', surface=grass_surface)
#         #                 if style == 'object':
#         #                     object_surf = graphics['object'][int(col)]
#         #                     Tile((x, y), [self.visible_sprites, self.obstacle_sprites], sprite_type='object', surface=object_surf)
#
#
#
#     def run(self):
#         # self.visible_sprites.draw(self.display_surface)
#         # self.visible_sprites.custom_draw(self.player)
#         # self.visible_sprites.update()
#         # DebugWriter.print(f'p_dir:{self.player.direction}')
#         # DebugWriter.print(f'p_center:{self.player.rect.center}')
