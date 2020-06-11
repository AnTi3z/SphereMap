import re
import time
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
            print(row.type.name)
            return row

    row_id = LocDescription.insert(txt_regexp=desc, type=1).execute()
    return LocDescription.get(LocDescription.id == row_id)


def add_event(room, desc, user_id):
    Events.insert(timestamp=time.time(), location=room, loc_desc=desc, user=user_id).execute()


def get_street(name):
    return Streets.get_or_none(Streets.name == name)


def get_room(x, y):
    return Rooms.get_or_none((Rooms.x == x) & (Rooms.y == y))
