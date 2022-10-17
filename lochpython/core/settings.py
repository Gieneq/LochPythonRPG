import pygame

WINDOW_TITLE = 'Tibia 2 in Python'

WIDTH, HEIGHT = 1200, 800
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2

FPS = 30
TILESIZE = 64
DEBUG = True
COLLISION_RANGE = TILESIZE

RESOURCES_ROOT = 'data'

GLOBAL_COOLDOWN = 500


class Init:
    screen = None

    def __init__(self):
        pygame.init()


if not Init.screen:
    Init.screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = Init.screen
