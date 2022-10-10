import pygame
from .settings import *
pygame.init()
font = pygame.font.Font(None, 30)

def text(x=10, y=10, msg='Working'):
    if DEBUG:
        display_surface = pygame.display.get_surface()
        text_surface = font.render(str(msg), True, 'White')
        text_rect = text_surface.get_rect(topleft = (x,y))
        pygame.draw.rect(display_surface, 'Black', text_rect)
        display_surface.blit(text_surface, text_rect)



