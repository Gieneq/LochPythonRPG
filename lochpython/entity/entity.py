from pygame.sprite import Sprite
from core.renderer import WorldRenderer

class Entity(Sprite):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.hitbox = None # uhh...

    def set_visible(self, visible):
        if visible:
            self.add(WorldRenderer.visible_objects)
        else:
            self.remove(WorldRenderer.visible_objects)

    def set_collideable(self, collideable):
        if collideable:
            self.add(self.world.obstacle_objects)
        else:
            self.remove(self.world.obstacle_objects)

    def collision(self, type, direction):
        if type == 'horizontal':
            for sprite in self.world.obstacle_objects:
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if type == 'vertical':
            for sprite in self.world.obstacle_objects:
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
