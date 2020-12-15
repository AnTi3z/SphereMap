import asyncio
import logging
import random
import time
from enum import Enum
# from typing import TypedDict, Optional, Final

from telethon import events, errors

# from telethon.tl.custom import MessageButton


logger = logging.getLogger('Sphere')
logger.setLevel(logging.INFO)


class Task(Enum):
    WALKING = 1
    STEALING = 2


# class State(TypedDict):
#     task: Optional[Task]
#     last_button: Optional[MessageButton]


# Global vars
BOT_ID = 944268265
global_state = {'task': None, 'last_button': None}


async def try_click(button):
    time.sleep(random.uniform(1.1, 2.5))
    global_state['last_button'] = button
    try:
        await button.click()
        global_state['last_button'] = None
    except errors.BotResponseTimeoutError:
        logger.warning(f"Button {button.data.decode()} answer timeout")
    except errors.MessageIdInvalidError:
        logger.warning(f"Message with {button.data.decode()} was deleted")


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
def activate():
    logger.info("Sphere script activated")


def deactivate():
    logger.info("Sphere script deactivated")


HANDLERS = (retry,)
