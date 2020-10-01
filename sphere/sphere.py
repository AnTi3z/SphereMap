import config
from modules import Module


def load(client):
    submodules = Module(client, config.configs['sphere'])
    for module_name in submodules.list_modules():
        submodules.load_module("sphere", module_name)
        if submodules.config['modules'][module_name]['enabled']:
            submodules.loaded_modules[module_name].activate(client)
