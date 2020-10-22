import importlib
import logging

logger = logging.getLogger('Modules')
logger.setLevel(logging.DEBUG)


class Modules:
    def __init__(self, client, cfg):
        self.loaded_modules = {}
        self.config = cfg
        self.client = client

    def list_modules(self):
        importlib.invalidate_caches()
        return self.config['modules'].keys()

    def load_module(self, directory, name):
        try:
            module = self.loaded_modules.get(name)
            if not module:
                module = importlib.import_module(f"{directory}.{name}")
                self.loaded_modules[name] = module
            else:
                module.deactivate(self.client)
                importlib.reload(module)

            logger.info(f"Module {directory}.{name} loaded")
            return module
        except Exception as e:
            logger.error(f"Module {directory}.{name} loading error: {e}")
            return None
