import logging
import random
import time

from telethon import events
from re import search

from .sphere import BOT_ID

logger = logging.getLogger('Sphere.fighting')
logger.setLevel(logging.DEBUG)

MODULE_CFG = {}

_fight_re = r'🧙🏻‍♂️.+\n❤️\d+.+🛡\d+.+\n\n.+\n❤️\d+.+🛡\d+'


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_fight_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_fight_re))
async def fighting(event):
    buttons_flat = [x for row in event.buttons[1:] for x in row if "🕐" not in x.text][:-1]
    pass


def activate():
    logger.info("Sphere.Fighting script activated")


def deactivate():
    logger.info("Sphere.Fighting script deactivated")


HANDLERS = (fighting,)
