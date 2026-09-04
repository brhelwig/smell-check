import json
import os

DEFAULT_CONFIG = {"unit": "seconds"}


def config_path(explicit=None):
    if explicit:
        return explicit
    return os.environ.get("PYTOOL_CONFIG", os.path.expanduser("~/.pytool.json"))


def cache_dir():
    return os.environ.get("PYTOOL_CACHE", os.path.expanduser("~/.cache/pytool"))


def load_config(explicit=None):
    path = config_path(explicit)
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(path):
        with open(path) as handle:
            config.update(json.load(handle))
    config["cache_dir"] = cache_dir()
    return config
