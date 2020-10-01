import importlib
import logging

logger = logging.getLogger('Modules')
logger.setLevel(logging.DEBUG)


class Module:
    def __init__(self, client, cfg):
        self.loaded_modules = {}
        self.config = cfg
        self.client = client

    def list_modules(self):
        importlib.invalidate_caches()
        return self.config['modules'].keys()

    def load_module(self, mod, name):
        try:
            module = self.loaded_modules.get(name)
            if not module:
                module = importlib.import_module(f"{mod}.{name}")
                self.loaded_modules[name] = module
            else:
                module.unload(self.client)
                importlib.reload(module)

            logger.info(f"Module {mod}.{name} loaded")
        except Exception as e:
            logger.error(f"Module {mod}.{name} loading error: {e}")

    def get_module(self, name):
        return self.loaded_modules.get(name)
