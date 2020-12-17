import asyncio
import logging
from enum import Enum
# from typing import Optional

from telethon import events

from button_clicker import ButtonClicker


logger = logging.getLogger('Sphere')
logger.setLevel(logging.INFO)


class Task(Enum):
    WALKING = 1
    STEALING = 2


# class State:
#     def __init__(self):
#         self.task: Optional[Task] = None


# Global vars
BOT_ID = 944268265
global_state = {'task': None}


# Не сработала кнопка
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"Не жми на кнопки так часто"))
async def retry(event):
    # Ждем 15 секунд
    await asyncio.sleep(15)
    await ButtonClicker.get_clicker(BOT_ID).reclick()


# Load submodules and activate them
def activate():
    logger.info("Sphere script activated")


def deactivate():
    logger.info("Sphere script deactivated")


HANDLERS = (retry,)
