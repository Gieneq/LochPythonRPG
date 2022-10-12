import pygame

from core.utils import import_folder
from core.settings import GLOBAL_COOLDOWN
# pygame.sprite.Sprite
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # self.world = world
        self.image = pygame.image.load('./data/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(100, 100))
        # self.hitbox = self.rect.inflate(0, -26)
        # self.set_visible(True)

        # self.import_player_assets()

        # self.direction = pygame.math.Vector2()
        # self.speed = 6
        # self.obstacle_sprites = world.obstacle_objects
        # self.cooldown = 0
        # self.cooldown_start_time = 0

    # def set_visible(self, visible):
    #     if visible:
    #         self.add(self.world.visible_objects)
    #     else:
    #         self.remove(self.world.visible_objects)
    #
    #
    # # def import_player_assets(self):
    # #     character_path = '../../data/graphics/player'
    # #     self.animations = {
    # #         'up': [],
    # #         'down': [],
    # #         'left': [],
    # #         'right': [],
    # #         'up_idle': [],
    # #         'down_idle': [],
    # #         'left_idle': [],
    # #         'right_idle': [],
    # #         'up_use': [],
    # #         'down_attack': [],
    # #         'left_attack': [],
    # #         'right_attack': [],
    # #     }
    # #
    # #     for animation in self.animations.keys():
    # #         path = character_path + '/' + animation
    # #         self.animations[animation] = import_folder(path)
    #
    # def input(self):
    #     keys = pygame.key.get_pressed()
    #
    #     # movement
    #     if keys[pygame.K_w]:
    #         self.direction.y = -1
    #     elif keys[pygame.K_s]:
    #         self.direction.y = 1
    #     else:
    #         self.direction.y = 0
    #
    #     if keys[pygame.K_a]:
    #         self.direction.x = -1
    #     elif keys[pygame.K_d]:
    #         self.direction.x = 1
    #     else:
    #         self.direction.x = 0
    #
    #     # use
    #     if keys[pygame.K_SPACE] and self.cooldown:
    #         self.cooldown_useup()
    #         print('use')
    #
    # def collision(self, direction):
    #     if direction == 'horizontal':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.x > 0:
    #                     self.hitbox.right = sprite.hitbox.left
    #                 if self.direction.x < 0:
    #                     self.hitbox.left = sprite.hitbox.right
    #
    #     if direction == 'vertical':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.y > 0:
    #                     self.hitbox.bottom = sprite.hitbox.top
    #                 if self.direction.y < 0:
    #                     self.hitbox.top = sprite.hitbox.bottom
    #
    # def move(self, speed):
    #     if self.direction.magnitude() != 0:
    #         self.direction = self.direction.normalize()
    #
    #     self.hitbox.x += self.direction.x * speed
    #     self.collision('horizontal')
    #     self.hitbox.y += self.direction.y * speed
    #     self.collision('vertical')
    #
    #     self.rect.center = self.hitbox.center
    #
    # def cooldown_update(self):
    #     curent_time = pygame.time.get_ticks()
    #     self.cooldown = min(0, self.cooldown_start_time - curent_time)
    #
    # def cooldown_useup(self):
    #     self.cooldown_start_time = pygame.time.get_ticks() + GLOBAL_COOLDOWN

    # def update(self):
    #     self.input()
    #     self.cooldown_update()
    #     self.move(self.speed)
