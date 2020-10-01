import logging
import importlib

from telethon import TelegramClient, events

# import mapper
# import walker
import config

logging.basicConfig(
    format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',
    datefmt='%H:%M:%S', level=logging.WARNING)

logger = logging.getLogger('UserbotCli')
logger.setLevel(logging.DEBUG)

loaded_modules = {}


@events.register(events.NewMessage(pattern=r"!load (.+)", outgoing=True))
async def load(event):
    load_module(event.pattern_match.group(1))


def list_modules():
    importlib.invalidate_caches()
    return config.load_config('modules')


def load_module(name):
    try:
        module = importlib.import_module(f"{name}.{name}")
        module.load(client)
        loaded_modules[name] = module
        logger.info(f"Module {name} loaded")
    except Exception as e:
        logger.error(f"Module {name} loading error: {e}")


if __name__ == "__main__":
    api = config.load_config('api')
    client = TelegramClient('AnTi3z', api['id'], api['hash'])
    client.start()

    for module_name in list_modules():
        if not loaded_modules.get(module_name):
            load_module(module_name)

    client.add_event_handler(load)
    client.run_until_disconnected()
