from telethon import events
import time
import random
import logging

btn_text = '🏌🏻'

logger = logging.getLogger('Krapiva')
logger.setLevel(logging.INFO)


# КРАПИВАААААААААААААА
@events.register(events.NewMessage(chats=(1196311609,), incoming=True))
async def krapiva(event):
    global btn_text
    time.sleep(random.uniform(0.9, 2.1))
    if event.reply_markup:
        btn_text = event.reply_markup.rows[0].buttons[0].text
    await event.client.send_message(1196311609, btn_text)


def activate(client):
    logger.info("Krapiva script activated")
    client.add_event_handler(krapiva)


def deactivate(client):
    logger.info("Krapiva script deactivated")
    client.remove_event_handler(krapiva)


# There is no submodules, activate this script
def load(client, _):
    activate(client)


def unload(client):
    deactivate(client)
