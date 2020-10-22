from modules import Modules

submodules: Modules


# Load submodules and activate them
def activate(client, cfg):
    global submodules
    submodules = Modules(client, cfg)
    for module_name in submodules.list_modules():
        module = submodules.load_module("sphere", module_name)
        module_cfg = cfg['modules'][module_name]
        if module and module_cfg['enabled']:
            module.activate(client, module_cfg)


def deactivate(client):
    if submodules:
        for module in submodules.loaded_modules.values():
            module.deactivate(client)
