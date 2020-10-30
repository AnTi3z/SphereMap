import asyncio
import logging
import random
import time

from telethon import events, TelegramClient

from .sphere import BOT_ID, global_state, Task


logger = logging.getLogger('Sphere.stealer')
logger.setLevel(logging.INFO)

# Global vars
client: TelegramClient

STEALER_CFG = {}


class StealTimer:
    def __init__(self):
        self._task = None

    @staticmethod
    def _set_steal():
        global_state['task'] = Task.STEALING
        logger.info("It's steal time!")

    def stop(self):
        if self._task:
            self._task.cancel()
            logger.debug(f"Steal timer stopped: {self._task}")

    def start(self, delay):
        self.stop()
        global_state['task'] = None
        delay_gap = delay + 15
        self._task = asyncio.get_event_loop().call_later(delay_gap, self._set_steal)
        logger.info(f"Steal timer started for {delay_gap} sec")


steal_timer = StealTimer()

_ready_re = r"(?s)^🧙🏻‍♂️.+❤️\d+.+🛡\d+.+👊"
_steal_re = r"(?s)^(?:Не найдя ничего лучше)|(?:Поискав подходящий случай)|(?:Побродив в округе)"
_wait_re = r"(?s)^Тебе пока рано снова воровать.+Через(?: (\d{1,2}) ч.)?(?: (\d{1,2}) м.)?(?: (\d{1,2}) с.)?"


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_ready_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_ready_re))
async def ready_handler(event):
    if global_state['task'] == Task.STEALING:
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🔮 Сфериум")
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🦹🏼‍♂️ Воровство")


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_steal_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_re))
async def steal_handler(event):
    btn = event.buttons[0][1]
    logger.debug(f"New steal message with button: {btn.data.decode()}")
    if global_state['task'] == Task.STEALING:
        logger.info(f"Click button: {btn.data.decode()}")
        await btn.click()

        steal_timer.start(1800)  # half hours

        await asyncio.sleep(random.uniform(200, 250))  # Gap fo fighting
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🔮 Сфериум")
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🏡 Прогулка по городу")


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_wait_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_wait_re))
async def wait_handler(event):
    time_remain = 0
    if event.pattern_match.group(1):
        time_remain += int(event.pattern_match.group(1)) * 3600  # hours
    if event.pattern_match.group(2):
        time_remain += int(event.pattern_match.group(2)) * 60  # minutes
    if event.pattern_match.group(3):
        time_remain += int(event.pattern_match.group(3))  # seconds

    steal_timer.start(1800)


_steal_money_re = r"(?s)^Ты выкрал из кошелька бедолаги 💰(\d+)!$"
_steal_fight_re = r"(?s)^Кража не удалась, драка неизбежна!$"
_steal_empty_re = r"(?s)^Увы, ничего украсть не удалось. Зато и не прилетело по башке.$"
_steal_box_re = r"(?s)^Тебе удалось украсть (.+)!$"  # контейнер
_steal_item_re = r"(?s)^Тебе удалось своровать (.+)!$"  # билет/ключ
_steal_stone_re = r"(?s)^Кража не удалась.+Защитный камень"


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_money_re))
async def steal1_handler(event):
    logger.info(f"Steal money: {event.pattern_match.group(1)}")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_fight_re))
async def steal2_handler(event):
    logger.info(f"Steal with fight!")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_empty_re))
async def steal3_handler(event):
    logger.info(f"Steal with nothing!")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_box_re))
async def steal4_handler(event):
    logger.info(f"Steal box: {event.pattern_match.group(1)}")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_item_re))
async def steal5_handler(event):
    logger.info(f"Steal jackpot: {event.pattern_match.group(1)}")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_stone_re))
async def steal6_handler(event):
    logger.info(f"Failed steal(stone)")


def activate(cli, cfg):
    global client
    global STEALER_CFG
    client = cli
    STEALER_CFG = cfg
    client.add_event_handler(ready_handler)
    client.add_event_handler(steal_handler)
    client.add_event_handler(wait_handler)
    client.add_event_handler(steal1_handler)
    client.add_event_handler(steal2_handler)
    client.add_event_handler(steal3_handler)
    client.add_event_handler(steal4_handler)
    client.add_event_handler(steal5_handler)
    client.add_event_handler(steal6_handler)
    logger.info("Stealer script activated")


def deactivate():
    if client:
        client.remove_event_handler(ready_handler)
        client.remove_event_handler(steal_handler)
        client.remove_event_handler(wait_handler)
        logger.info("Stealer script deactivated")
