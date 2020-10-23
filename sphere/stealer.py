import logging
import asyncio
import time
import random

from telethon import events, functions

from . import tasks
from .sphere import BOT_ID

STEALER_CFG = {}

steal_list = []

logger = logging.getLogger('Sphere.stealer')
logger.setLevel(logging.INFO)


class StealTimer:
    def __init__(self):
        self._task = None

    @staticmethod
    def set_steal():
        tasks.CURRENT_TASK = tasks.Task.STEALING
        logger.info("It's steal time!")

    def stop(self):
        if self._task:
            self._task.cancel()
            logger.debug(f"Steal timer stopped: {self._task}")

    def set(self, delay):
        self.stop()
        tasks.CURRENT_TASK = tasks.Task.NONE
        steal_list.clear()
        delay_gap = delay + 15
        self._task = asyncio.get_event_loop().call_later(delay_gap, StealTimer.set_steal)
        logger.info(f"Steal timer started for {delay_gap} sec")


steal_timer = StealTimer()


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=r"(?s)^🧙🏻‍♂️.+❤️\d+.+🛡\d+.+👊"))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=r"(?s)^🧙🏻‍♂️.+❤️\d+.+🛡\d+.+👊"))
async def ready_handler(event):
    attempts_left = STEALER_CFG["attempts"] - len(steal_list)
    if tasks.CURRENT_TASK == tasks.Task.STEALING and attempts_left > 0:
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.respond("🔮 Сфериум")
        for _ in range(attempts_left):
            time.sleep(random.uniform(1.1, 2.5))
            await event.message.respond("🦹🏼‍♂️ Воровство")


@events.register(events.MessageEdited(
    chats=(944268265,),
    pattern=r"(?s)^(?:Не найдя ничего лучше)|(?:Поискав подходящий случай)|(?:Побродив в округе)")
)
@events.register(events.NewMessage(
    chats=(944268265,),
    pattern=r"(?s)^(?:Не найдя ничего лучше)|(?:Поискав подходящий случай)|(?:Побродив в округе)")
)
async def steal_handler(event):
    logger.debug(f"New steal message with button: {event.reply_markup.rows[0].buttons[1].data.decode('utf-8')}")
    steal_list.append((event.id, event.reply_markup.rows[0].buttons[1].data.decode('utf-8')))
    logger.debug(f"Steal list: {steal_list}")
    if tasks.CURRENT_TASK == tasks.Task.STEALING and len(steal_list) >= STEALER_CFG["attempts"]:
        msg_id, btn_data = random.choice(steal_list)
        logger.debug(f"Push! msg:{msg_id} btn_data: {btn_data}")
        await event.client(
            functions.messages.GetBotCallbackAnswerRequest(event.from_id,
                                                           msg_id,
                                                           data=btn_data.encode("utf-8"))
        )

        steal_timer.set(7200)  # two hours

        await asyncio.sleep(random.uniform(200, 250))  # Gap fo fighting
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.respond("🔮 Сфериум")
        time.sleep(random.uniform(1.1, 2.5))
        await event.message.respond("🏡 Прогулка по городу")


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
        time_remain += int(event.pattern_match.group(1)) * 3600  # hours
    if event.pattern_match.group(2):
        time_remain += int(event.pattern_match.group(2)) * 60  # minutes
    if event.pattern_match.group(3):
        time_remain += int(event.pattern_match.group(3))  # seconds

    steal_timer.set(time_remain)


def activate(client, stealer_cfg):
    global STEALER_CFG
    STEALER_CFG = stealer_cfg
    client.add_event_handler(ready_handler)
    client.add_event_handler(steal_handler)
    client.add_event_handler(wait_handler)
    logger.info("Stealer script activated")


def deactivate(client):
    client.remove_event_handler(ready_handler)
    client.remove_event_handler(steal_handler)
    client.remove_event_handler(wait_handler)
    logger.info("Stealer script deactivated")
