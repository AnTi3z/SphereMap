import logging
import random
import time

from telethon import events

from .sphere import BOT_ID

logger = logging.getLogger('Sphere.fighting')
logger.setLevel(logging.INFO)

MODULE_CFG = {}

_fight_re = r'🧙🏻‍♂️.+\n❤️\d+.+🛡\d+.*\n\n.+\n❤️\d+.+🛡\d+'


def sphere_choose(buttons):
    buttons_flat = [x for row in buttons for x in row if "🕐" not in x.text]
    if len(buttons_flat) == 1:
        return buttons_flat[0]
    else:
        buttons_flat = buttons_flat[:-1]

    for sphere in MODULE_CFG['build']:
        for button in buttons_flat:
            if sphere in button.text:
                return button

    return buttons_flat[-1]


@events.register(events.MessageEdited(chats=(BOT_ID,), pattern=_fight_re))
@events.register(events.NewMessage(chats=(BOT_ID,), pattern=_fight_re))
async def fighting(event):
    if event.buttons is None:
        return

    time.sleep(random.uniform(3.0, 7.5))
    single_button = event.buttons[0][0]
    if "В бой" in single_button.text:
        logger.debug(f"In to the battle clicked!")
        await single_button.click()
    else:
        await sphere_choose(event.buttons[1:]).click()


def activate():
    logger.info("Sphere.Fighting script activated")


def deactivate():
    logger.info("Sphere.Fighting script deactivated")


HANDLERS = (fighting,)
