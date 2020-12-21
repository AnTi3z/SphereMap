import asyncio
import logging
from enum import Enum

from telethon import events

from button_clicker import ButtonClicker


logger = logging.getLogger('Sphere')
logger.setLevel(logging.INFO)


class Task(Enum):
    NONE = 1
    WALKING = 2
    STEALING = 3


class State:
    def __init__(self):
        self.task = Task.NONE

    def is_no_tasks(self):
        return self.task == Task.NONE


# Global vars
BOT_ID = 944268265
global_state = State()


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
