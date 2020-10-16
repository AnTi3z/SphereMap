import logging
import asyncio
import time
import random

from telethon import events, functions

from . import tasks

ATTEMPTS = 0


logger = logging.getLogger('Sphere.stealer')
logger.setLevel(logging.DEBUG)


@events.register(events.MessageEdited(chats=(944268265,), pattern=r"(?s)^🧙🏻‍♂️.+❤️\d+.+🛡\d+.+👊"))
@events.register(events.NewMessage(chats=(944268265,), pattern=r"(?s)^🧙🏻‍♂️.+❤️\d+.+🛡\d+.+👊"))
async def ready_handler(event):
    if tasks.CURRENT_TASK == tasks.Task.STEALING:
        time.sleep(random.uniform(1.1, 2.5))
        await event.client.send_message(944268265, "🔮 Сфериум")
        for _ in range(ATTEMPTS):
            time.sleep(random.uniform(1.1, 2.5))
            await event.client.send_message(944268265, "🦹🏼‍♂️ Воровство")


@events.register(events.MessageEdited(
    chats=(944268265,),
    pattern=r"(?s)^(?:Не найдя ничего лучше)|(?:Поискав подходящий случай)|(?:Побродив в округе)")
)
@events.register(events.NewMessage(
    chats=(944268265,),
    pattern=r"(?s)^(?:Не найдя ничего лучше)|(?:Поискав подходящий случай)|(?:Побродив в округе)")
)
async def steal_handler(event):
    if tasks.CURRENT_TASK == tasks.Task.STEALING:
        print("ВОРУЕМ")


@events.register(events.MessageEdited(
    chats=(944268265,),
    pattern=r"(?s)^Тебе пока рано снова воровать.+через(?: (\d{1,2}) ч.)?(?: (\d{1,2}) м.)?(?: (\d{1,2}) с.)?")
)
@events.register(events.NewMessage(
    chats=(944268265,),
    pattern=r"(?s)^Тебе пока рано снова воровать.+через(?: (\d{1,2}) ч.)?(?: (\d{1,2}) м.)?(?: (\d{1,2}) с.)?")
)
async def wait_handler(event):
    time_remain = 0
    if event.pattern_match.group(1):
        time_remain += int(event.pattern_match.group(1)) * 3600
    if event.pattern_match.group(2):
        time_remain += int(event.pattern_match.group(2)) * 60
    if event.pattern_match.group(3):
        time_remain += int(event.pattern_match.group(3))

    tasks.CURRENT_TASK = tasks.Task.WALKING
    logger.info(f"Таймер воровства установлен на {time_remain+15} сек")
    await asyncio.sleep(time_remain+15)
    tasks.CURRENT_TASK = tasks.Task.STEALING


def activate(client, stealer_cfg):
    global ATTEMPTS
    ATTEMPTS = stealer_cfg["attempts"]
    client.add_event_handler(ready_handler)
    client.add_event_handler(wait_handler)
    logger.info("Stealer script activated")


def deactivate(client):
    client.remove_event_handler(ready_handler)
    client.remove_event_handler(wait_handler)
    logger.info("Stealer script deactivated")
