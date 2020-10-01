import logging

from telethon import TelegramClient, events

import config
from modules import Module

logging.basicConfig(
    format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',
    datefmt='%H:%M:%S', level=logging.WARNING)

logger = logging.getLogger('UserbotCli')
logger.setLevel(logging.DEBUG)


@events.register(events.NewMessage(pattern=r"!load (.+)", outgoing=True))
async def load(event):
    modules.load_module(event.pattern_match.group(1))


if __name__ == "__main__":
    api = config.load_config('api')
    client = TelegramClient('AnTi3z', api['id'], api['hash'])
    client.start()

    modules = Module(client, config.load_config())
    for module_name in modules.list_modules():
        config.configs[module_name] = config.load_config(file=f"{module_name}/config.json")
        modules.load_module(module_name, module_name)
        modules.loaded_modules[module_name].load(modules.client)

    client.add_event_handler(load)
    client.run_until_disconnected()
