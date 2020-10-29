import logging
import random
import time

from telethon import events, TelegramClient

btn_text = '🏌🏻'

logger = logging.getLogger('Krapiva')
logger.setLevel(logging.INFO)

BOT_ID = 1196311609
client: TelegramClient


# КРАПИВАААААААААААААА
@events.register(events.NewMessage(chats=(BOT_ID,), incoming=True))
async def krapiva(event):
    global btn_text
    time.sleep(random.uniform(0.9, 2.1))
    if event.reply_markup:
        btn_text = event.reply_markup.rows[0].buttons[0].text
    await event.message.respond(btn_text)


# There is no submodules, activate this script with no config
def activate(cli, _):
    global client
    client = cli
    client.add_event_handler(krapiva)
    logger.info("Krapiva script activated")


def deactivate():
    if client:
        client.remove_event_handler(krapiva)
        logger.info("Krapiva script deactivated")
