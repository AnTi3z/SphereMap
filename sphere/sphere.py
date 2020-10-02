from modules import Modules


def load(client, cfg):
    submodules = Modules(client, cfg)
    for module_name in submodules.list_modules():
        submodules.load_module("sphere", module_name)
        if submodules.config['modules'][module_name]['enabled']:
            submodules.loaded_modules[module_name].activate(client)
