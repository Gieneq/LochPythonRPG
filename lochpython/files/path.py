import os
from typing import NamedTuple
from core import settings


def remove_extension(file_name):
    return file_name.split('.')[0]

class ResourceFiles:
    TILESETS = settings.GRAPHICS_TILESETS_PATHS
    ENTITIES = settings.GRAPHICS_ENTITIES_PATHS
    MAPS = settings.MAPS_PATH
    File = NamedTuple('File', [('name', str), ('abs_path', str)])

    def __init__(self, root):
        self.root = root
        self.ignore_workspace = True

    def get_childs_names(self):
        child_dirs = os.listdir(self.root)
        child_dirs = list(filter(lambda path: path != settings.IGNORE_WORKSPACE_DIR, child_dirs))
        return child_dirs

    def get_files(self, file_type) -> list[File]:
        file_type = file_type.lower()
        childs_names = self.get_childs_names()
        filered_childs_names = [child_name for child_name in childs_names if child_name.lower().endswith(file_type)]
        return [self.File(name=child_name, abs_path=os.path.join(self.root, child_name)) for child_name in
                filered_childs_names]

    def get_tsx_files(self):
        return self.get_files('tsx')
    def get_tmx_files(self):
        return self.get_files('tmx')
