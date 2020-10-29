import logging
import random
import time

from telethon import events, TelegramClient

logger = logging.getLogger('bs_digger')
logger.setLevel(logging.INFO)

BOT_ID = 764095451
client: TelegramClient


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"(?s).+Копать еще:", incoming=True))
async def digging(event):
    time.sleep(random.uniform(10, 100))
    await event.message.respond(r"/dig")


def activate(cli, _):
    global client
    client = cli
    client.add_event_handler(digging)
    logger.info("BS digger script activated")


def deactivate():
    if client:
        client.remove_event_handler(digging)
        logger.info("BS digger script deactivated")
