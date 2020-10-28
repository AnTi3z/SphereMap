import asyncio
import logging
from enum import Enum

from telethon import events, functions, errors

from modules import Modules

logger = logging.getLogger('Sphere')
logger.setLevel(logging.INFO)


class Task(Enum):
    WALKING = 1
    STEALING = 2
    NONE = 3


BOT_ID = 944268265
submodules: Modules

global_state = {
    "task": Task.NONE,
    "last_button": None
}


# Не сработала кнопка
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"Не жми на кнопки так часто"))
async def retry(event):
    # Ждем 15 секунд
    await asyncio.sleep(15)
    if global_state['last_button']:
        try:
            logger.debug(f"Button {['last_button'][1]} retry click")
            await event.client(
                functions.messages.GetBotCallbackAnswerRequest(event.from_id,
                                                               global_state['last_button'][0],
                                                               data=global_state['last_button'][1].encode("utf-8"))
            )
            # Кнопка прожалась, все ок
            global_state['last_button'] = None
            logger.info(f"Button {['last_button'][1]} retry click success")
        except errors.BotResponseTimeoutError:
            # Кнопка не прожалась, возможно придется пробовать еще
            logger.warning(f"Button {['last_button'][1]} answer timeout")
        except errors.MessageIdInvalidError:
            global_state['last_button'] = None
            logger.warning(f"Message with {['last_button'][1]} was deleted while retry click")


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
