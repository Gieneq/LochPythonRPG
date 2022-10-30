from enum import Enum

from lochpython.objects.property import Props


class GameObject:
    # todo remove prop execute after render, need to remove queue

    class GOType(Enum):
        BASEMENT = 0
        OBJECTS = 1

    def __init__(self):
        self.properties = {}
        # consider if properties can be needed multiple times
        self._input_handlers = []
        self._update_handlers = []
        self._render_handlers = []
        self.containers = {
            'input': self._input_handlers,
            'update': self._update_handlers,
            'render': self._render_handlers,
        }

    def add_property(self, name, prop):
        self.properties[name] = prop
        for name, container in self.containers.items():
            if hasattr(prop, name):
                container.append(prop)

    def has_property(self, name):
        return name in self.properties.keys()

    # builder

    def with_sprite(self, prop):
        self.add_property(Props.SPRITE, prop)
        return self

    def with_collision(self, prop):
        self.add_property(Props.COLLISION, prop)
        return self

    def with_moving(self, prop):
        self.add_property(Props.MOVING, prop)
        return self

    def with_wsad(self, prop):
        self.add_property(Props.WSAD_DRIVEN, prop)
        return self

    def with_animation(self, prop):
        self.add_property(Props.ANIMATION, prop)
        return self

    def with_light_source(self, prop):
        self.add_property(Props.LIGHT_SOURCE, prop)
        return self

    def with_emitter(self, prop):
        self.add_property(Props.EMITTER, prop)
        return self

    def with_particle(self, prop):
        self.add_property(Props.PARTICLE, prop)
        return self

    # general loop methods

    def input(self, *args, **kwargs):
        for handler in self._input_handlers:
            handler.input(*args, **kwargs)

    def update(self, *args, **kwargs):
        for handler in self._update_handlers:
            handler.update(*args, **kwargs)

    def render(self, *args, **kwargs):
        for handler in self._render_handlers:
            handler.render(*args, **kwargs)
