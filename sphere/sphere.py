from modules import Modules


def load(client, cfg):
    submodules = Modules(client, cfg)
    for module_name in submodules.list_modules():
        submodules.load_module("sphere", module_name)
        module = submodules.loaded_modules[module_name]
        if module and submodules.config['modules'][module_name]['enabled']:
            module.activate(client)
