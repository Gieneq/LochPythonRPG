from math import sqrt

from pygame import Rect
from pygame.math import Vector2

from core.debug import Debugger
from core.utils import distance_squared, radius_squared_from_rect
from objects.go import GameObject
from objects.property import Props, AnimationPlayer
from world.worldloader import WorldLoader, PlayerLoader
from core.renderer import WorldRenderer
from core.settings import COLLISION_RANGE, RENDERING_HEIGHT, RENDERING_WIDTH, FOV_OFFSET


class Camera(Vector2):
    def __init__(self, focus_point=Vector2(0, 0), inertial=True):
        super().__init__()
        self.xy = focus_point
        self.inertial = inertial
        self.target_pos = Vector2(self)
        self.velocity = Vector2(0, 0)
        self.focused_rect = Rect((0,0), (1,1))
        self.speed = 4.5
        self.fov_rect = Rect(focus_point, (RENDERING_WIDTH, RENDERING_HEIGHT))

    def focus_on_entity(self, rect, refresh=True):
        self.focused_rect = rect
        if refresh:
            self.xy = self.focused_rect.center

    def update_camera(self, dt):
        if self.focused_rect:
            self.target_pos = self.focused_rect.center

        if not self.inertial:
            self.xy = self.target_pos
        else:
            self.xy += dt * self.velocity
            self.velocity = (self.target_pos - self.xy) * self.speed

        self.fov_rect.w, self.fov_rect.h = RENDERING_WIDTH, RENDERING_HEIGHT
        self.fov_rect.centerx, self.fov_rect.centery = self.xy
        self.fov_rect = self.fov_rect.inflate(FOV_OFFSET, FOV_OFFSET)

    def __str__(self):
        return f"Looking at: {self.focused_rect} {self.target_pos}, has pos: {self.xy}, vel: {self.velocity}"


class Layer(list):
    # def __init__(self, *args):
    #     super().__init__()

    def update(self, *args, **kwargs):
        for item in self:
            item.update(*args, **kwargs)

    def input(self, *args, **kwargs):
        for item in self:
            item.input(*args, **kwargs)

    def render(self, *args, **kwargs):
        for item in self:
            item.render(*args, **kwargs)


class World:
    def __init__(self):
        self._basement = Layer()
        self._objects = Layer()

        self.global_timers = []
        self.nature_timer = AnimationPlayer(frames_count=4, duration=5)  # todo
        self.global_timers.append(self.nature_timer)

        self.stack = Layer([self._basement, self._objects])

        self.colliding_objects = []

        WorldLoader.load_test_map(self)
        self.player = PlayerLoader(self).load((350, 200))
        self.add_game_object(self.player, GameObject.GOType.OBJECTS)
        # self._objects.append(self.player) # hm?
        self.camera = Camera()
        self.camera.focus_on_entity(self.player.properties[Props.SPRITE].rect)

    def input(self):
        self.stack.input()

    def update(self, dt):
        self.stack.update(dt=dt)
        self.camera.update_camera(dt=dt)
        for global_timer in self.global_timers:
            global_timer.update(dt=dt)

        # FOV
        # fov_rect = self.camera.get_field_of_view()
        # done inside sprite property - toggle visible

    def render(self):
        self.stack.render()

    def on_player_move(self):
        WorldRenderer.sort_order()

    def is_near(self, hitbox_1, hitbox_2):
        dist = sqrt(distance_squared(hitbox_1.center, hitbox_2.center))
        r1 = sqrt(radius_squared_from_rect(hitbox_1))
        r2 = sqrt(radius_squared_from_rect(hitbox_2))
        return dist - r1 - r2 < COLLISION_RANGE

    def get_nearby_obstacles(self, coll_prop):
        potentially_colliding_objects = filter(lambda x: self.is_near(x.hitbox, coll_prop.hitbox),
                                               self.colliding_objects)
        potentially_colliding_objects = filter(lambda x: x is not coll_prop, potentially_colliding_objects)
        potentially_colliding_objects = set(potentially_colliding_objects)

        potentially_colliding_objects = list(potentially_colliding_objects)
        return potentially_colliding_objects

    @property
    def limit_blocks_count(self):
        return len(self.colliding_objects)
    @property
    def basement_tiles_count(self):
        return len(self._basement)
    @property
    def objects_count(self):
        return len(self._objects)

    def add_game_object(self, go, go_type):
        if go_type == 0:
            self._basement.append(go)
        else:
            self._objects.append(go)

    def get_objects(self, go_type, position):
        layer = self._basement if go_type == GameObject.GOType.BASEMENT else self._objects
        return list(filter(lambda go: go.properties[Props.SPRITE].rect.topleft == position, layer))
