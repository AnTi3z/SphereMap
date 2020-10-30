import logging

from telethon import TelegramClient, events

import config
from modules import Modules

logging.basicConfig(
    format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',
    datefmt='%H:%M:%S', level=logging.WARNING)

logger = logging.getLogger('UserbotCli')
logger.setLevel(logging.DEBUG)

# Global vars
client: TelegramClient
modules: Modules


def load_module(name):
    module = modules.load_module(name, name)
    if module and modules.config['modules'][name]['enabled']:
        try:
            module_cfg = config.load_config(file=f"{name}/config.json")
        except FileNotFoundError as e:
            module_cfg = None
            logger.error(e)
        module.activate(client, module_cfg)


@events.register(events.NewMessage(pattern=r"!load (.+)", outgoing=True))
async def load(event):
    load_module(event.pattern_match.group(1))


if __name__ == "__main__":
    # Telegram connect
    api = config.load_config('api')
    client = TelegramClient('AnTi3z', api['id'], api['hash'])
    client.start()

    # Load script modules
    modules = Modules(config.load_config())
    for module_name in modules.list_modules():
        load_module(module_name)

    client.add_event_handler(load)
    client.run_until_disconnected()
