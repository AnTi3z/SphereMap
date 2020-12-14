import importlib
import logging

import config

logger = logging.getLogger('Modules')
logger.setLevel(logging.DEBUG)


class Module:
    CLIENT = None
    ROOT_MOD = None

    def __init__(self, name: str, enabled=True, parent=None):
        self.name = name
        self.enabled = enabled
        self._parent = parent
        self._submodules = set()

        if name != "_ROOT_":
            cfg = None
            # it's one of main modules
            if self._parent.name == "_ROOT_":
                cfg = config.load_config(file=f"{name}/config.json")
            # it's a submodule
            elif self._parent:
                cfg = self._parent.modules_cfg[name]
            self._module = self._load()
            self._module.MODULE_CFG = cfg
        else:
            cfg = config.load_config()

        if cfg and 'modules' in cfg:
            self.modules_cfg = cfg['modules']
            self._load_submodules()

    @classmethod
    def load_modules(cls, client):
        cls.CLIENT = client
        cls.ROOT_MOD = Module("_ROOT_")
        for module in cls.ROOT_MOD._submodules:
            if module.enabled:
                module.activate()
        return cls.ROOT_MOD

    def get_by_name(self, name):
        if name == self.name:
            return self
        for mod in self._submodules:
            result = mod.get_by_name(name)
            if result:
                return result
        return None

    def _load_submodules(self):
        for module_name in self.modules_cfg:
            module = Module(module_name, self.modules_cfg[module_name]['enabled'], self)
            self._submodules.add(module)

    def _load(self):
        dir_name = self._parent.name if self._parent.name != "_ROOT_" else self.name
        module = importlib.import_module(f"{dir_name}.{self.name}")
        return module

    def reload(self):
        if self._module:
            self._module = importlib.reload(self._module)
        # else:
        #     self._module = self._load()
        # for sub_mod in self._submodules:
        #     sub_mod.reload()

    def activate(self):
        self._module.activate()
        for handler in self._module.HANDLERS:
            self.CLIENT.add_event_handler(handler)
        for module in self._submodules:
            if module.enabled:
                module.activate()

    def deactivate(self):
        for module in self._submodules:
            module.deactivate()
        for handler in self._module.HANDLERS:
            self.CLIENT.remove_event_handler(handler)
        self._module.deactivate()

# class RootModule(Module):
#     def __init__(self, client):
#         super().CLIENT = client
#         super().__init__("_ROOT_")
#
#     def activate(self):
#         pass
#
#     def deactivate(self):
#         pass
