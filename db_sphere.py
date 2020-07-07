import re
import logging
from db_models import *

logger = logging.getLogger('SphereMap')


def add_street(x, name):
    Streets.insert(x=x, name=name).on_conflict_ignore().execute()
    return get_street(name)


def add_room(x, y):
    Rooms.insert(x=x, y=y).on_conflict_ignore().execute()
    return get_room(x, y)


def add_passage(start, end):
    return Passages.insert(start=start, end=end).on_conflict_ignore().execute()


def check_description(desc):
    query = LocDescription.select()
    for row in query:
        if re.search(row.txt_regexp, desc):
            return row

    row_id = LocDescription.insert(txt_regexp=desc, type=1).execute()
    return LocDescription.get(LocDescription.id == row_id)


def add_event(room, desc, user_id, date, entry):
    event_id = Events.insert(timestamp=int(date.timestamp()), location=room, loc_desc=desc, user=user_id).execute()
    if entry:
        EntryPoints.insert(event=event_id).execute()


def get_street(name):
    return Streets.get_or_none(Streets.name == name)


def get_room(x, y):
    return Rooms.get_or_none((Rooms.x == x) & (Rooms.y == y))


def get_last_room_stat(user_id):
    event = Events.select().join(Users).order_by(Events.timestamp.desc()).where(Users.tg_id == user_id).get()
    room = event.location
    query = (Events
             .select(Events, fn.COUNT(EventTypes.id).alias('cnt'))
             .join(LocDescription)
             .join(EventTypes)
             .where(Events.location == room)
             .group_by(EventTypes.id)
             .order_by(EventTypes.id))
    stats = {
        "event_id": event.id,
        "name": room.street.name,
        "num": room.y,
        "last_type": event.loc_desc.type.name,
        "entry": EntryPoints.select().join(Events).where(Events.location == room).count(),
        "portal_exit": PortalExits.select().join(Events).where(Events.location == room).count(),
        "events": [(ev.loc_desc.type.name, ev.cnt) for ev in query]
    }
    return stats
