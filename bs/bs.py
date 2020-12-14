import logging
import random
import time

from telethon import events

logger = logging.getLogger('bs_digger')
logger.setLevel(logging.INFO)

BOT_ID = 764095451


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"(?s).+Копать еще:", incoming=True))
async def digging(event):
    time.sleep(random.uniform(10, 100))
    await event.respond(r"/dig")


def activate():
    logger.info("BS digger script activated")


def deactivate():
    logger.info("BS digger script deactivated")


HANDLERS = (digging,)
