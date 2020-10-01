import json
from contextlib import contextmanager


def load_config(key=None):
    with open('config.json', 'r', encoding='utf-8') as read_file:
        cfg = json.load(read_file)
        return cfg.get(key) if key else cfg


@contextmanager
def reader(key=None):
    yield load_config(key)
