import logging
import random
import time

from telethon import events

from .sphere import BOT_ID, global_state, Task
from timer import Timer

logger = logging.getLogger('Sphere.stealer')
logger.setLevel(logging.INFO)

MODULE_CFG = {}

steal_timer = Timer(lambda: setattr(global_state, 'task', Task.STEALING), "StealTimer")
steal_fighting = False

_ready_re = r"(?s)^🧙🏻‍♂️.+❤️\d+.+🛡\d+.+👊"
_steal_re = r"(?s)^(?:Не найдя ничего лучше)|(?:Поискав подходящий случай)|(?:Побродив в округе)"
_wait_re = r"(?s)^Тебе пока рано искать жертву.+Через(?: (\d{1,2}) ч.)?(?: (\d{1,2}) м.)?(?: (\d{1,2}) с.)?"


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_ready_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_ready_re))
async def ready_handler(event):
    if global_state.task == Task.STEALING:
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🔮 Сфериум")
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🦹🏼‍♂️ Воровство")


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_steal_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_re))
async def steal_handler(event):
    btn = event.buttons[0][1]
    logger.debug(f"New steal message with button: {btn.data.decode()}")
    if global_state.task == Task.STEALING:
        logger.info(f"Click button: {btn.data.decode()}")
        await btn.click()

        global_state.task = Task.NONE
        steal_timer.start(1800+15)  # half hours


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
    logger.debug(f"Steal search time remain: {time_remain}")

    global_state.task = Task.NONE
    steal_timer.start(time_remain-5400+15)


_steal_money_re = r"(?s)^Ты выкрал.+💰(\d+)"
_steal_box_re = r"(?s)^Тебе удалось украсть (.+)!"  # контейнер
_steal_item_re = r"(?s)^Тебе удалось своровать (.+)!"  # билет/ключ
_steal_fight_re = r"(?s)^Кража не удалась, (?:драка|сражение)"
_steal_empty_re = r"(?s)^Увы, ничего украсть не удалось. Зато и не прилетело по башке."
_steal_stone_re = r"(?s)^Кража не удалась.+Защитный камень"


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_money_re))
async def steal1_handler(event):
    logger.info(f"Steal money: {event.pattern_match.group(1)}")
    time.sleep(random.uniform(1.1, 2.5))
    await event.respond("🏘 Бараки")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_box_re))
async def steal2_handler(event):
    logger.info(f"Steal box: {event.pattern_match.group(1)}")
    time.sleep(random.uniform(1.1, 2.5))
    await event.respond("🏘 Бараки")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_item_re))
async def steal3_handler(event):
    logger.info(f"Steal jackpot: {event.pattern_match.group(1)}")
    time.sleep(random.uniform(1.1, 2.5))
    await event.respond("🏘 Бараки")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_fight_re))
async def steal4_handler(event):
    global steal_fighting
    steal_fighting = True
    logger.info(f"Steal with fight!")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_empty_re))
async def steal5_handler(event):
    logger.info(f"Steal with nothing!")
    time.sleep(random.uniform(1.1, 2.5))
    await event.respond("🏘 Бараки")


@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_steal_stone_re))
async def steal6_handler(event):
    logger.info(f"Failed steal(stone)")
    time.sleep(random.uniform(1.1, 2.5))
    await event.respond("🏘 Бараки")


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern="(?s)Показать лог боя:"))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern="(?s)Показать лог боя:"))
async def fight_end(event):
    global steal_fighting
    if steal_fighting:
        steal_fighting = False
        time.sleep(random.uniform(1.1, 2.5))
        await event.respond("🏘 Бараки")


def activate():
    logger.info("Sphere.Stealer script activated")


def deactivate():
    logger.info("Sphere.Stealer script deactivated")


HANDLERS = (ready_handler, steal_handler, wait_handler,
            steal1_handler, steal2_handler, steal3_handler,
            steal4_handler, steal5_handler, steal6_handler,
            fight_end)
