from pygame.rect import Rect
from pygame.sprite import Sprite

from core.debug import Debugger
from core.renderer import WorldRenderer


class Entity(Sprite):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.hitbox = None  # uhh...

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


    def eval_collision(self, translation, obstacles):
        self.hitbox.x += translation[0]
        for obstacle in obstacles:
            if obstacle.hitbox.colliderect(self.hitbox):
                self.eval_collision_x(translation[0], obstacle.hitbox)

        self.hitbox.y += translation[1]
        for obstacle in obstacles:
            if obstacle.hitbox.colliderect(self.hitbox):
                self.eval_collision_y(translation[1], obstacle.hitbox)


    def eval_collision_x(self, translation_x, obstacle_hitbox):
        if translation_x > 0:
            self.hitbox.right = obstacle_hitbox.left
        if translation_x < 0:
            self.hitbox.left = obstacle_hitbox.right

    def eval_collision_y(self, translation_y, obstacle_hitbox):
        if translation_y > 0:
            self.hitbox.bottom = obstacle_hitbox.top
        if translation_y < 0:
            self.hitbox.top = obstacle_hitbox.bottom

    def move(self, speed, direction):
        if direction.magnitude() != 0:
            direction = direction.normalize()

        # todo dt
        translation = direction * speed
        obstacles = self.world.get_nearby_obstacles(self)
        self.eval_collision(translation, obstacles)
        # print(dir(self.hitbox))
        # self.hitbox.x += translation[0]
        # self.hitbox.y += translation[1]

        self.rect.center = self.hitbox.center

        # todo moze ial niezerowy dir w sciane
        self.world.on_player_move()
