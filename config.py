import json


def load_config(key=None, file='config.json'):
    with open(file, 'r', encoding='utf-8') as read_file:
        cfg = json.load(read_file)
        return cfg.get(key) if key else cfg
