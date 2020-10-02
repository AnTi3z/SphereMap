from modules import Modules


# Load submodules and activate them
def activate(client, cfg):
    submodules = Modules(client, cfg)
    for module_name in submodules.list_modules():
        module = submodules.load_module("sphere", module_name)
        module_cfg = cfg['modules'][module_name]
        if module and module_cfg['enabled']:
            module.activate(client, module_cfg)


def deactivate(client):
    pass
