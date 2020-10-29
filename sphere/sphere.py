import asyncio
import logging
from enum import Enum
from typing import TypedDict, Optional

from telethon import events, errors
from telethon.tl.custom import MessageButton

from modules import Modules

logger = logging.getLogger('Sphere')
logger.setLevel(logging.INFO)


class Task(Enum):
    WALKING = 1
    STEALING = 2
    NONE = 3


BOT_ID = 944268265
submodules: Modules

global_state = TypedDict('global_state',
                         {'task': Optional[Task], 'last_button': Optional[MessageButton]})


# Не сработала кнопка
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"Не жми на кнопки так часто"))
async def retry(event):
    # Ждем 15 секунд
    await asyncio.sleep(15)
    if global_state['last_button']:
        btn_data = global_state['last_button'].data.decode()
        try:
            logger.debug(f"Button {btn_data} retry click")
            await global_state['last_button'].click()
            # Кнопка прожалась, все ок
            global_state['last_button'] = None
            logger.info(f"Button {btn_data} retry click success")
        except errors.BotResponseTimeoutError:
            # Кнопка не прожалась, возможно придется пробовать еще
            logger.warning(f"Button {btn_data} answer timeout")
        except errors.MessageIdInvalidError:
            global_state['last_button'] = None
            logger.warning(f"Message with {btn_data} was deleted while click retry")


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
