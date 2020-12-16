import logging
import random
import time

from telethon import events
from re import search

from .sphere import BOT_ID

logger = logging.getLogger('Sphere.combiner')
logger.setLevel(logging.INFO)

MODULE_CFG = {}

_boxes_re = r'Коробочки:'


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_boxes_re))
async def combiner(event):
    if MODULE_CFG['enabled']:
        for level in range(MODULE_CFG['level']+1):
            if search(fr'/union_{level}', event.text):
                time.sleep(random.uniform(1.1, 2.5))
                await event.respond(f"/union_conf_{level}")
                break


def activate():
    logger.info("Sphere.Combiner script activated")


HANDLERS = (combiner,)
