import logging
import random
import time

from telethon import events

logger = logging.getLogger('Krapiva')
logger.setLevel(logging.INFO)

BOT_ID = 1196311609


# КРАПИВАААААААААААААА
@events.register(events.NewMessage(chats=(BOT_ID,), incoming=True))
async def krapiva(event):
    time.sleep(random.uniform(1.1, 2.1))
    if event.buttons:
        await event.click(0)


# There is no submodules, activate this script with no config
def activate():
    logger.info("Krapiva script activated")


def deactivate():
    logger.info("Krapiva script deactivated")


HANDLERS = (krapiva,)
