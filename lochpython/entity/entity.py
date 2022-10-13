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
        o_encountered_x = self.eval_collision_x(translation, obstacles)
        o_encountered_y = self.eval_collision_y(translation, obstacles)
        return list(set(o_encountered_x + o_encountered_y))

    def eval_collision_x(self, translation, obstacles):
        obstacles_encountered = []
        self.hitbox.x += translation[0]
        for obstacle in obstacles:
            if obstacle.hitbox.colliderect(self.hitbox):
                obstacles_encountered.append(obstacle)
                if translation[0] > 0:
                    self.hitbox.right = obstacle.hitbox.left
                if translation[0] < 0:
                    self.hitbox.left = obstacle.hitbox.right
        return obstacles_encountered

    def eval_collision_y(self, translation, obstacles):
        obstacles_encountered = []
        self.hitbox.y += translation[1]
        for obstacle in obstacles:
            if obstacle.hitbox.colliderect(self.hitbox):
                obstacles_encountered.append(obstacle)
                if translation[1] > 0:
                    self.hitbox.bottom = obstacle.hitbox.top
                if translation[1] < 0:
                    self.hitbox.top = obstacle.hitbox.bottom
        return obstacles_encountered

    def move(self, speed, dt, direction):
        if direction.magnitude() != 0:
            direction = direction.normalize()

        translation = direction * speed * dt
        obstacles = self.world.get_nearby_obstacles(self)
        obstacles_encountered = self.eval_collision(translation, obstacles)
        for obstacle in obstacles_encountered:
            Debugger.rect(obstacle.hitbox, 'Yellow', 5)

        self.rect.center = self.hitbox.center

        # todo moze ial niezerowy dir w sciane
        self.world.on_player_move()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        Debugger.rect(self.rect, 'Red')
        Debugger.rect(self.hitbox, 'Blue')
