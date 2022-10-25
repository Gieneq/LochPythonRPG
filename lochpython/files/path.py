import os

from core.settings import IGNORE_WORKSPACE_DIR

def remove_extension(file_name):
    return file_name.split('.')[0]

def load_dirs(resource_dir):
    return os.listdir(resource_dir)


def ignore_workspace(paths):
    return list(filter(lambda path: path != IGNORE_WORKSPACE_DIR, paths))


def build_abs_paths(parent, children):
    return list(os.path.join(parent, child) for child in children)


def get_resource_abs_path(resource_dir):
    resulting_dirs = list(ignore_workspace(load_dirs(resource_dir)))
    return list(zip(resulting_dirs, build_abs_paths(resource_dir, resulting_dirs)))


def filter_path_by_type(paths_tuple, filetype):
    filetype_lower = filetype.lower()
    return [path for path in paths_tuple if path[0].lower().endswith(filetype_lower)]
