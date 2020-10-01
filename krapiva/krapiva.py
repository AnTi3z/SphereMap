from telethon import events
import time
import random

btn_text = '🏌🏻'


# КРАПИВАААААААААААААА
@events.register(events.NewMessage(chats=(1196311609,), incoming=True))
async def krapiva(event):
    global btn_text
    time.sleep(random.uniform(0.9, 2.1))
    if event.reply_markup:
        btn_text = event.reply_markup.rows[0].buttons[0].text
    await event.client.send_message(1196311609, btn_text)


def activate(client):
    client.add_event_handler(krapiva)


def load(client):
    activate(client)
