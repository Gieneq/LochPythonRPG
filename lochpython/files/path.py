import os

from core.settings import IGNORE_WORKSPACE_DIR


def load_dirs(resource_dir):
    return os.listdir(resource_dir)


def ignore_workspace(paths):
    return filter(lambda path: path != IGNORE_WORKSPACE_DIR, paths)


def build_abs_paths(parent, children):
    return (os.path.join(parent, child) for child in children)


def get_resource_abs_path(resource_dir):
    resulting_dirs = list(ignore_workspace(load_dirs(resource_dir)))
    return resulting_dirs, build_abs_paths(resource_dir, resulting_dirs)


def filter_path_by_type(paths, filetype):
    filetype_lower = filetype.lower()
    paths_lower = (path.lower() for path in paths)
    return [path for path in paths_lower if path.endswith(filetype_lower)]
