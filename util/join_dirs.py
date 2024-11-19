import os


def join_dirs(prefix, suffix):
    name = os.path.join(prefix, suffix)
    os.makedirs(name, exist_ok=True)
    return name
