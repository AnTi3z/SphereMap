import logging
import random
import time
import itertools

from telethon import events, errors

from .sphere import BOT_ID, global_state

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
    time.sleep(random.uniform(1.1, 2.5))
    for btn in itertools.chain.from_iterable(event.buttons):
        if btn.data.decode() == 'frabuildbuild':
            await try_click(btn)


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


def activate():
    logger.info("Sphere.Builder script activated")


def deactivate():
    logger.info("Sphere.Builder script deactivated")


HANDLERS = (go_to_buildings, start_build)
