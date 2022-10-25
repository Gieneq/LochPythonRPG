import pygame
import os

WINDOW_TITLE = 'Tibia 2 in Python'
DISPLAY_DIVISOR = 1
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1800 // DISPLAY_DIVISOR, 900 // DISPLAY_DIVISOR

SCALE = 4
RENDERING_WIDTH, RENDERING_HEIGHT = DISPLAY_WIDTH / SCALE, DISPLAY_HEIGHT / SCALE
HALF_RENDERING_WIDTH, HALF_RENDERING_HEIGHT = RENDERING_WIDTH // 2, RENDERING_HEIGHT // 2

FPS = 30
TILESIZE = 20
DEBUG = True
DEBUG_VISIBLE_OBJECTS = False
DEBUG_COLLISION_BLOCKS = True
COLLISION_RANGE = TILESIZE

GLOBAL_COOLDOWN = 500
FOV_OFFSET = 4 * TILESIZE

"""Graphics resources"""
IGNORE_WORKSPACE_DIR = 'workspace'
RESOURCES_ROOT = '../../data'
GRAPHICS_TILESETS_PATHS = os.path.join(RESOURCES_ROOT, 'tilesets')
GRAPHICS_ENTITIES_PATHS = os.path.join(RESOURCES_ROOT, 'entities')
MAPS_PATH = os.path.join(RESOURCES_ROOT, 'maps')

"""Initial"""


class Init:
    screen = None

    def __init__(self):
        pass


if not Init.screen:
    pygame.init()
    Init.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
# screen = Init.screen
