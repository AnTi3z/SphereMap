import logging

from telethon import TelegramClient, events

import config
from modules import Modules

logging.basicConfig(
    format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',
    datefmt='%H:%M:%S', level=logging.WARNING)

logger = logging.getLogger('UserbotCli')
logger.setLevel(logging.DEBUG)

modules = None


def load_module(name):
    try:
        cfg = config.load_config(file=f"{name}/config.json")
    except FileNotFoundError as e:
        cfg = None
        logger.error(e)
    modules.load_module(name, name)
    module = modules.loaded_modules.get(name)
    if module:
        module.load(modules.client, cfg)


@events.register(events.NewMessage(pattern=r"!load (.+)", outgoing=True))
async def load(event):
    load_module(event.pattern_match.group(1))


if __name__ == "__main__":
    api = config.load_config('api')
    client = TelegramClient('AnTi3z', api['id'], api['hash'])
    client.start()

    modules = Modules(client, config.load_config())
    for module_name in modules.list_modules():
        load_module(module_name)

    client.add_event_handler(load)
    client.run_until_disconnected()
