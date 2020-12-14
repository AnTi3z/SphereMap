import json
import os.path


def load_config(key=None, file='config.json'):
    if not os.path.exists(file):
        print(f"file not found: {file}")
        return None

    with open(file, 'r', encoding='utf-8') as read_file:
        cfg = json.load(read_file)
        return cfg.get(key) if key else cfg
