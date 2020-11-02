import logging
import re
import itertools

from telethon import events, TelegramClient

import sphere.db_sphere as db_sphere
from .db_models import *

logger = logging.getLogger('Sphere.mapper')
logger.setLevel(logging.INFO)

bandit = False
entry = False
client: TelegramClient


def db_room_parse(room, user, date, entry_flag=False):
    logger.debug(f"ROOM: {room}")
    with database.connection_context():
        for passage in room["exits"]:
            Streets.get_or_create(x=passage["x"], name=passage["street"])
            Rooms.get_or_create(x=passage["x"], y=passage["y"])

        street = Streets.get_or_none(Streets.name == room["street"])
        if street:
            (current_room, _) = Rooms.get_or_create(x=street, y=room["num"])
            for passage in room["exits"]:
                (end_room, _) = Rooms.get_or_create(x=passage["x"], y=passage["y"])
                Passages.get_or_create(start=current_room, end=end_room)
        else:
            current_room = None
            logger.warning(f"No '{room['street']}' street found in DB.")

        desc = db_sphere.check_description(room["desc"])
        if current_room:
            event = Events.create(timestamp=int(date.timestamp()), location=current_room, loc_desc=desc, user=user)
            if entry_flag:
                EntryPoints.create(event=event)
            return event


@events.register(events.NewMessage(chats=(944268265,), pattern=r"(?s)^Тебе удалось одолеть городского"))
async def bandit_handler(event):
    global bandit
    # TODO: Проверить, что это не гражданин
    bandit = True


@events.register(events.NewMessage(chats=(944268265,), pattern=r"(?s)^Ты начал гулять по городу"))
async def entry_handler(event):
    global entry
    entry = True


@events.register(events.MessageEdited(chats=(944268265,), pattern=r"(?s)^Ты находишься на 🏡(.+?) (\d+)\s+(.+)"))
@events.register(events.NewMessage(chats=(944268265,), pattern=r"(?s)^Ты находишься на 🏡(.+?) (\d+)\s+(.+)"))
async def town_handler(event):
    global bandit
    global entry
    entry_flag = entry
    bandit_flag = bandit
    entry = False
    bandit = False
    room = {"street": event.pattern_match.group(1),
            "num": int(event.pattern_match.group(2)),
            "desc": event.pattern_match.group(3),
            "exits": list()}
    if bandit_flag:
        room["desc"] = "Тебе удалось одолеть городского"
    for btn in itertools.chain.from_iterable(event.buttons):
        txt = re.search(r"(?s)🏡 (\d+) (.+)", btn.text)
        data = btn.data.decode().split('_')
        if txt and data[0] == "cwgoto":
            room["exits"].append({
                "street": txt.group(2).replace("\n", " "),
                "num": int(txt.group(1)),
                "x": int(data[1]),
                "y": int(data[2])
            })
    date = event.edit_date or event.date
    db_room_parse(room, event.to_id.user_id, date, entry_flag)
    await event.client.inline_query('SpheriumMapperBot', "new_map_event")


def activate(cli, _):
    global client
    client = cli
    client.add_event_handler(bandit_handler)
    client.add_event_handler(entry_handler)
    client.add_event_handler(town_handler)
    logger.info("Mapper script activated")


def deactivate():
    if client:
        client.remove_event_handler(bandit_handler)
        client.remove_event_handler(entry_handler)
        client.remove_event_handler(town_handler)
        logger.info("Mapper script deactivated")
