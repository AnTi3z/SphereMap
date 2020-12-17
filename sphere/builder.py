import logging
import random
import time

from telethon import events

from .sphere import BOT_ID
from button_clicker import ButtonClicker

logger = logging.getLogger('Sphere.builder')
logger.setLevel(logging.INFO)

MODULE_CFG = {}

_build_re = r'Ты решил отдохнуть, взять перекур и ушёл со стройки.'
_buildings_re = r'Постройки фракции:'


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_build_re))
async def go_to_buildings(event):
    time.sleep(random.uniform(1.1, 2.5))
    await event.respond(r"/buildings")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_buildings_re))
async def start_build(event):
    await ButtonClicker.get_clicker(BOT_ID).click_cb_data(event, 'frabuildbuild')


def activate():
    logger.info("Sphere.Builder script activated")


def deactivate():
    logger.info("Sphere.Builder script deactivated")


HANDLERS = (go_to_buildings, start_build)
