from telethon import events
import time
import random
import logging

logger = logging.getLogger('bs_digger')
logger.setLevel(logging.INFO)

BOT_ID = 764095451


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"(?s).+Копать еще:", incoming=True))
async def digging(event):
    time.sleep(random.uniform(10, 100))
    await event.message.respond(r"/dig")


def activate(client, _):
    logger.info("BS digger script activated")
    client.add_event_handler(digging)


def deactivate(client):
    logger.info("BS digger script deactivated")
    client.remove_event_handler(digging)
