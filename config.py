import json
from contextlib import contextmanager


def load_config(key):
    with open('config.json', 'r', encoding='utf-8') as read_file:
        return json.load(read_file).get(key)


@contextmanager
def reader(key):
    yield load_config(key)
