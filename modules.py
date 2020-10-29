import importlib
import logging

logger = logging.getLogger('Modules')
logger.setLevel(logging.DEBUG)


class Modules:
    def __init__(self, cfg):
        self.loaded_modules = {}
        self.config = cfg

    def list_modules(self):
        importlib.invalidate_caches()
        return self.config['modules'].keys()

    def load_module(self, directory, name):
        module = self.loaded_modules.get(name)
        try:
            if not module:
                module = importlib.import_module(f"{directory}.{name}")
            else:
                module.deactivate()
                module = importlib.reload(module)
        except Exception as e:
            logger.error(f"Module {directory}.{name} loading error: {e}")
            return None

        self.loaded_modules[name] = module
        logger.info(f"Module {directory}.{name} loaded")
        return module
