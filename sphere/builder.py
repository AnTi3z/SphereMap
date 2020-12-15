import logging
import random
import time

from telethon import events, errors

from .sphere import BOT_ID, global_state

logger = logging.getLogger('Sphere.builder')
logger.setLevel(logging.INFO)


BUILDER_CFG = {}

_build_re = r'Ты решил отдохнуть, взять перекур и ушёл со стройки.'
_buildings_re = r'Постройки фракции:'


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_build_re))
async def go_to_buildings(event):
    if BUILDER_CFG['enabled']:
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.respond("/buildings")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_buildings_re))
async def start_build(event):
    if BUILDER_CFG['enabled']:
        time.sleep(random.uniform(1.1, 2.5))
        await try_click(event.message, 'frabuildbuild')
        return


async def try_click(msg, data):
    time.sleep(random.uniform(1.1, 2.5))
    global_state['last_button'] = (msg.id, data)
    try:
        await msg.click(data=data.encode('utf-8'))
        global_state['last_button'] = None
    except errors.BotResponseTimeoutError:
        logger.warning(f"Button {data} answer timeout")
    except errors.MessageIdInvalidError:
        logger.warning(f"Message with {data} was deleted")


def activate(client, builder_cfg):
    global BUILDER_CFG
    BUILDER_CFG = builder_cfg
    client.add_event_handler(go_to_buildings)
    client.add_event_handler(start_build)
    logger.info("Builder script activated")


def deactivate(client):
    client.remove_event_handler(go_to_buildings)
    client.remove_event_handler(start_build)
    logger.info("Builder script deactivated")
